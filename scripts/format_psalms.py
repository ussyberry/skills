import zipfile
import re
import pathlib
import xml.etree.ElementTree as ET
import copy

# Namespaces
NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main' # for xlsx
}

def register_namespaces():
    for prefix, uri in NS.items():
        ET.register_namespace(prefix, uri)

def get_psalm_titles(xlsx_path):
    titles = {} # Num -> Title
    try:
        with zipfile.ZipFile(xlsx_path) as z:
            # Get Shared Strings
            shared_strings = []
            if 'xl/sharedStrings.xml' in z.namelist():
                xml_data = z.read('xl/sharedStrings.xml')
                root = ET.fromstring(xml_data)
                ns = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'} # xlsx namespace
                for t in root.findall('.//a:t', ns):
                    shared_strings.append(t.text)
            
            # Get Sheet Data
            if 'xl/worksheets/sheet1.xml' in z.namelist():
                xml_data = z.read('xl/worksheets/sheet1.xml')
                root = ET.fromstring(xml_data)
                ns = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                
                rows = root.findall('.//a:row', ns)
                # Skip header row (1)
                for row in rows:
                    cells = row.findall('.//a:c', ns)
                    row_vals = []
                    for cell in cells:
                         cell_type = cell.get('t')
                         val_tag = cell.find('a:v', ns)
                         value = val_tag.text if val_tag is not None else ""
                         if cell_type == 's' and value.isdigit():
                             idx = int(value)
                             if idx < len(shared_strings):
                                 value = shared_strings[idx]
                         row_vals.append(value)
                    
                    if len(row_vals) >= 2:
                        p_num = row_vals[0]
                        p_title = row_vals[1]
                        
                        # Normalize num (remove 'PSALM ' if present, or just int)
                        if str(p_num).strip().isdigit():
                            titles[int(p_num)] = p_title.strip()
                            
    except Exception as e:
        print(f"Error reading xlsx: {e}")
    return titles

def create_drop_cap_para(char, original_ppr):
    # Create a new Paragraph for the Drop Cap
    # <w:p>
    #   <w:pPr>
    #     <w:framePr w:dropCap="drop" w:lines="3" w:wrap="around" w:vAnchor="text" w:hSpace="113" w:y="0"/>
    #     <w:rPr> ... </w:rPr>
    #   </w:pPr>
    #   <w:r>
    #     <w:t>C</w:t>
    #   </w:r>
    # </w:p>
    
    p = ET.Element(f"{{{NS['w']}}}p")
    pPr = ET.Element(f"{{{NS['w']}}}pPr")
    
    # Frame Properties for Drop Cap
    framePr = ET.Element(f"{{{NS['w']}}}framePr")
    framePr.set(f"{{{NS['w']}}}dropCap", "drop")
    framePr.set(f"{{{NS['w']}}}lines", "3")
    framePr.set(f"{{{NS['w']}}}wrap", "around")
    framePr.set(f"{{{NS['w']}}}vAnchor", "text")
    framePr.set(f"{{{NS['w']}}}hSpace", "113") 
    pPr.append(framePr)
    
    # Copy specialized styling if needed? Usually just defaults
    # But font matching matters.
    # Let's assume standard font (Garamond from file name)
    
    p.append(pPr)
    
    r = ET.Element(f"{{{NS['w']}}}r")
    rPr = ET.Element(f"{{{NS['w']}}}rPr")
    font = ET.Element(f"{{{NS['w']}}}rFonts")
    font.set(f"{{{NS['w']}}}ascii", "Garamond")
    font.set(f"{{{NS['w']}}}hAnsi", "Garamond")
    rPr.append(font)
    
    # Size? Drop caps are usually large but the Frame property scales them automatically to 'lines=3'.
    r.append(rPr)
    
    t = ET.Element(f"{{{NS['w']}}}t")
    t.text = char
    r.append(t)
    p.append(r)
    
    return p

def process_docx(src, dest, titles):
    with zipfile.ZipFile(src) as zin:
        with zipfile.ZipFile(dest, 'w') as zout:
            for item in zin.infolist():
                content = zin.read(item.filename)
                
                if item.filename == 'word/document.xml':
                    register_namespaces()
                    root = ET.fromstring(content)
                    body = root.find(f"{{{NS['w']}}}body")
                    
                    # We need to iterate and structurally modify.
                    # Copying elements to a list first handles modification index issues.
                    elements = list(body)
                    
                    new_elements = []
                    
                    skip_next = False
                    
                    for i, elem in enumerate(elements):
                        if skip_next: 
                            skip_next = True # wait this logic is flawed if I don't reset or use while loop
                            # Actually easier: iterate valid elements
                            pass
                    
                    # Better approach: Rebuild Body
                    body_children = []
                    
                    # Flag to insert Drop Cap on NEXT paragraph
                    pending_drop_cap = False
                    
                    for elem in elements:
                        if elem.tag != f"{{{NS['w']}}}p":
                            body_children.append(elem)
                            continue
                        
                        # It's a paragraph. Inspect Text.
                        # Naive text extraction (fast)
                        txt = "".join([t.text for t in elem.findall(f".//{{{NS['w']}}}t") if t.text])
                        
                        # Check for PSALM Header
                        psalm_match = re.match(r'^\s*PSALM\s+(\d+)', txt, re.IGNORECASE)
                        if psalm_match:
                            p_num = int(psalm_match.group(1))
                            print(f"Processing Psalm {p_num}")
                            
                            # Update Header: PSALM X <br> Title
                            # Clear runs
                            for r in elem.findall(f"{{{NS['w']}}}r"):
                                elem.remove(r)
                            
                            # Add New Run
                            r = ET.Element(f"{{{NS['w']}}}r")
                            t1 = ET.Element(f"{{{NS['w']}}}t")
                            t1.text = f"PSALM {p_num}"
                            
                            br = ET.Element(f"{{{NS['w']}}}br")
                            
                            t2 = ET.Element(f"{{{NS['w']}}}t")
                            title = titles.get(p_num, "")
                            t2.text = title
                            
                            r.append(t1)
                            r.append(br)
                            r.append(t2)
                            elem.append(r)
                            
                            body_children.append(elem)
                            pending_drop_cap = True
                            
                        elif pending_drop_cap and txt.strip():
                            # This is the Body Paragraph!
                            # Apply Drop Cap
                            
                            clean_text = txt.lstrip() # Remove leading spaces
                            if not clean_text:
                                body_children.append(elem)
                                continue

                            first_char = clean_text[0]
                            rest_text = clean_text[1:]
                            
                            # 1. Create Drop Cap Para
                            # Pass original pPr to inherit font? logic inside func handles basics
                            # Currently standard Garamond
                            drop_para = create_drop_cap_para(first_char, elem.find(f"{{{NS['w']}}}pPr"))
                            body_children.append(drop_para)
                            
                            # 2. Modify Current Para (Remove first char)
                            # We need to find *which* run had the first char.
                            # Complex finding logic:
                            char_removed = False
                            runs = elem.findall(f"{{{NS['w']}}}r")
                            for r in runs:
                                texts = r.findall(f"{{{NS['w']}}}t")
                                for t in texts:
                                    if t.text and t.text.strip():
                                        # This is the start
                                        # We assume first non-empty text node has the char
                                        # (Edge case: First char might be split?)
                                        # Simplified: Remove first char from this node text
                                        stripped = t.text.lstrip()
                                        if len(stripped) > 0:
                                            # We found it
                                            # We need to account for space logic?
                                            # Word usually handles leading space in xml:space="preserve"
                                            # Let's just strip leading, take 1st char (already stored), remove it.
                                            
                                            # Find index of first char
                                            val = t.text
                                            match = re.search(r'\S', val)
                                            if match:
                                                idx = match.start()
                                                # New val
                                                new_val = val[idx+1:]
                                                t.text = new_val
                                                char_removed = True
                                                break
                                if char_removed: break
                            
                            body_children.append(elem)
                            pending_drop_cap = False
                        
                        else:
                            # Normal paragraph
                            body_children.append(elem)
                            
                    # Clear body and append new children
                    body.clear()
                    for c in body_children:
                        body.append(c)
                        
                    content = ET.tostring(root, encoding='utf-8', xml_declaration=True) # Check if standalone works
                
                zout.writestr(item, content)

    print(f"Created formatted file: {dest}")

def main():
    base = pathlib.Path("BOOK OF PSALMS")
    xlsx = base / "TOC Psalms.xlsx"
    # Use the UPDATED file as source? No, use the source "garamond drop" file because update script just hacked xml string
    # Actually, the user "replaced the word document" earlier, but the update script ran on "garamond drop_Updated"
    # Let's run on "garamond drop.docx" fresh to avoid conflicting edits, 
    # OR run on "garamond drop_Updated.docx" if we want to preserve titles we just added?
    # BUT this script RE-ADDS titles properly from XLSX. So fresh source is better/safer.
    src = base / "THE PRAYER BOOK OF PSALMS - garamond drop.docx" 
    dest = base / "THE PRAYER BOOK OF PSALMS - Final.docx"
    
    titles = get_psalm_titles(xlsx)
    print(f"Loaded {len(titles)} titles.")
    process_docx(src, dest, titles)

if __name__ == "__main__":
    main()
