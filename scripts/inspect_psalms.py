import zipfile
import re
import pathlib
import xml.etree.ElementTree as ET

def get_docx_text(path):
    try:
        with zipfile.ZipFile(path) as z:
            xml_content = z.read('word/document.xml').decode('utf-8')
            # Rudimentary XML tag stripping
            text = re.sub('<[^>]+>', ' ', xml_content)
            # Collapse whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            return text
    except Exception as e:
        return f"Error reading docx: {e}"

def get_xlsx_data(path):
    try:
        with zipfile.ZipFile(path) as z:
            # 1. Get Shared Strings
            shared_strings = []
            if 'xl/sharedStrings.xml' in z.namelist():
                xml_data = z.read('xl/sharedStrings.xml')
                root = ET.fromstring(xml_data)
                # Schema: http://schemas.openxmlformats.org/spreadsheetml/2006/main
                ns = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                for t in root.findall('.//a:t', ns):
                    shared_strings.append(t.text)
            
            # 2. Get Sheet Data
            rows = []
            if 'xl/worksheets/sheet1.xml' in z.namelist():
                xml_data = z.read('xl/worksheets/sheet1.xml')
                root = ET.fromstring(xml_data)
                ns = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                
                # Iterate rows
                for row in root.findall('.//a:row', ns):
                    row_data = []
                    # Iterate cells
                    for cell in row.findall('.//a:c', ns):
                        cell_type = cell.get('t')
                        val_tag = cell.find('a:v', ns)
                        value = val_tag.text if val_tag is not None else ""
                        
                        if cell_type == 's' and value.isdigit():
                            # Shared string index
                            idx = int(value)
                            if idx < len(shared_strings):
                                value = shared_strings[idx]
                        row_data.append(value)
                    rows.append(row_data)
            
            return rows
    except Exception as e:
        return [f"Error: {e}"]

def inspect_psalms():
    base_path = pathlib.Path("BOOK OF PSALMS")
    docx_file = base_path / "THE PRAYER BOOK OF PSALMS - Final.docx"
    xlsx_file = base_path / "TOC Psalms.xlsx"

    print(f"--- Inspecting {xlsx_file.name} ---")
    if xlsx_file.exists():
        rows = get_xlsx_data(xlsx_file)
        print("First 10 Rows of Data:")
        for r in rows[:10]:
            print(r)
    else:
        print("File not found.")
    
    print("\n" + "="*50 + "\n")

    print(f"--- Inspecting {docx_file.name} ---")
    if docx_file.exists():
        # Check header
        try:
            with open(docx_file, 'rb') as f:
                header = f.read(10)
                print(f"File Header (Hex): {header.hex()}")
                if header.startswith(b'PK'):
                    print("Format: Zip (DOCX/XLSX)")
                    docx_text = get_docx_text(docx_file)
                    print(f"Total Text Length: {len(docx_text)} chars")
                    print("Excerpt:")
                    print(docx_text[:2000] + "...")
                elif header.hex().upper().startswith("D0CF11E0"):
                    print("Format: OLE Compound File (Old .doc or .xls)")
                    print("Cannot read .doc format natively with standard libraries.")
                elif header.startswith(b'{\\rtf'):
                    print("Format: RTF")
                    print("Text content likely visible in raw ascii but messy.")
                elif header.startswith(b'%PDF'):
                    print("Format: PDF renamed as DOCX")
                else:
                    print("Unknown format.")
        except Exception as e:
            print(f"Error checking header: {e}")

    else:
        print("File not found.")

if __name__ == "__main__":
    inspect_psalms()
