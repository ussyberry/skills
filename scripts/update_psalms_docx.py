import zipfile
import re
import pathlib
import shutil

def update_psalms():
    base_path = pathlib.Path("BOOK OF PSALMS")
    src_file = base_path / "THE PRAYER BOOK OF PSALMS - garamond drop.docx"
    dest_file = base_path / "THE PRAYER BOOK OF PSALMS - garamond drop_Updated.docx"
    
    # Titles to insert
    # Looking at the patterns in the doc, title usually follows "PSALM X" 
    # Current text: "PSALM 1 Blessed is..."
    # Desired: "PSALM 1 The Way of the Righteous and the End of the Ungodly Blessed is..."
    # Note: We need to be careful with XML tags. We will try to find the plain text "PSALM 1" in the xml and append title.
    # However, "PSALM 1" might be split across <w:t> tags. 
    # Simpler regex on the full XML string usually works if we assume standard simple text runs, but Word splits text arbitrarily.
    # Since we saw "THE PRAYER BOOK OF PSALMS PSALM 1 Blessed" in the text extraction, it's likely contiguous or close.
    
    title_1 = " The Way of the Righteous and the End of the Ungodly"
    title_2 = " The Messiah's Triumph and Kingdom"
    
    with zipfile.ZipFile(src_file, 'r') as zin:
        with zipfile.ZipFile(dest_file, 'w') as zout:
            for item in zin.infolist():
                content = zin.read(item.filename)
                
                if item.filename == 'word/document.xml':
                    xml_str = content.decode('utf-8')
                    
                    # Heuristic replacement:
                    # Look for "PSALM 1" pattern. 
                    # Attempt 1: Simple string replace if in same run
                    # Use a regex that allows for some XML tags in between if possible, but that's risky.
                    # Let's try to find the exact text run first.
                    
                    # Case 1: "PSALM 1" is in text. 
                    if "PSALM 1" in xml_str and title_1.strip() not in xml_str:
                         print("Found PSALM 1...")
                         # Check if "Blessed" follows
                         # We want to insert Title before "Blessed" or immediately after "PSALM 1" and likely a paragraph break.
                         # In simple XML edit, we just add text. Formatting might be merged.
                         # Ideally we add a <w:br/> or similar.
                         
                         # Let's just insert the text for now.
                         xml_str = xml_str.replace("PSALM 1", f"PSALM 1{title_1} <w:br/> ")
                    
                    if "PSALM 2" in xml_str and title_2.strip() not in xml_str:
                         print("Found PSALM 2...")
                         xml_str = xml_str.replace("PSALM 2", f"PSALM 2{title_2} <w:br/> ")
                         
                    content = xml_str.encode('utf-8')
                
                zout.writestr(item, content)

    print(f"Created updated file: {dest_file}")

if __name__ == "__main__":
    update_psalms()
