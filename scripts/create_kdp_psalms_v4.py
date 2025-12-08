import zipfile
import re
import pathlib
import xml.etree.ElementTree as ET
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import portrait
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate, Table, TableStyle, PageBreak, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors
import os

# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------
PAGE_WIDTH = 6.0 * inch
PAGE_HEIGHT = 9.0 * inch

# Margins
TOP_MARGIN = 0.75 * inch
BOTTOM_MARGIN = 0.75 * inch
INSIDE_MARGIN = 0.75 * inch
OUTSIDE_MARGIN = 0.50 * inch

FONT_NAME = 'Times-Roman' 
BODY_FONT_SIZE = 12
LEADING = 12 * 1.15 

OUTPUT_FILENAME = "Psalms_6x9_Final_v4.pdf"
INPUT_DOCX = "BOOK OF PSALMS/THE PRAYER BOOK OF PSALMS - garamond drop.docx"
INPUT_XLSX = "BOOK OF PSALMS/TOC Psalms.xlsx"

# ------------------------------------------------------------------
# DATA EXTRACTION
# ------------------------------------------------------------------

def get_psalm_titles(xlsx_path):
    titles = {}
    try:
        with zipfile.ZipFile(xlsx_path) as z:
            # Shared Strings
            shared = []
            if 'xl/sharedStrings.xml' in z.namelist():
                root = ET.fromstring(z.read('xl/sharedStrings.xml'))
                ns = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                for t in root.findall('.//a:t', ns):
                    shared.append(t.text)
            
            # Sheet
            if 'xl/worksheets/sheet1.xml' in z.namelist():
                root = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
                ns = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                for row in root.findall('.//a:row', ns):
                    vals = []
                    for cell in row.findall('.//a:c', ns):
                        t = cell.get('t')
                        v = cell.find('a:v', ns)
                        val = v.text if v is not None else ""
                        if t == 's' and val.isdigit():
                            val = shared[int(val)]
                        vals.append(val)
                    
                    if len(vals) >= 2:
                        p_num = vals[0]
                        p_title = vals[1]
                        if str(p_num).strip().isdigit():
                            titles[int(p_num)] = p_title.strip()
    except Exception as e:
        print(f"Error reading extracted titles: {e}")
    return titles

def clean_text(text):
    replacements = [
        ("AMorning", "A Morning Prayer for Protection"),
        ("ASong", "A Song"),
        ("Oppessors", "Oppressors"),
        ("Workshop", "Worship"),
        ("  ", " "),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text

def normalize(s):
    """Remove spaces and punctuation for comparison."""
    return re.sub(r'[\W_]+', '', s).lower()

def extract_psalms(docx_path, titles_map):
    psalms = []
    current_psalm = None
    
    try:
        with zipfile.ZipFile(docx_path) as z:
            root = ET.fromstring(z.read('word/document.xml'))
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            for p in root.findall('.//w:p', ns):
                texts = [t.text for t in p.findall('.//w:t', ns) if t.text]
                full_text = "".join(texts)
                full_text = clean_text(full_text)
                
                if not full_text.strip():
                    continue
                
                header_match = re.search(r'^\s*PSALM\s+(\d+)', full_text, re.IGNORECASE)
                
                if header_match:
                    p_num = int(header_match.group(1))
                    
                    # Remove "PSALM X" from start
                    remainder = full_text[header_match.end():].strip()
                    p_title = titles_map.get(p_num, "")
                    
                    current_psalm = {
                        'number': p_num,
                        'title': p_title,
                        'body_paragraphs': []
                    }
                    psalms.append(current_psalm)
                    
                    # Duplication Handling for START of Psalm
                    # Logic: If p_title is present, check if 'remainder' contains it.
                    # We only strip if p_num >= 3 (per user instruction) OR generally safe?
                    # User says "all apart from psalm 1 and 2 have duplicate headers".
                    # Safe to check for ALL: if body starts with title, strip it.
                    
                    stripped_remainder = remainder
                    if p_title:
                        # Robust Check: Normalize both
                        norm_title = normalize(p_title)
                        norm_rem = normalize(remainder)
                        
                        if norm_rem.startswith(norm_title):
                            # It matches! We need to cut the raw string carefully.
                            # Since normalization removes chars, finding exact cut index is tricky.
                            # Heuristic: Remove len(p_title) characters + any leading/trailing junk?
                            # Better: Regex match with ignoring spaces?
                            # Simple approach: If exact string (ignoring case) matches:
                            if remainder.lower().startswith(p_title.lower()):
                                stripped_remainder = remainder[len(p_title):].strip()
                            else:
                                # Fuzzy match fallback:
                                # If the normalized startsWith, then likely the first few words match.
                                # Let's try to remove it if it's "close enough"
                                pass # Keep safe to avoid cutting verses.
                    
                    if stripped_remainder:
                        current_psalm['body_paragraphs'].append(stripped_remainder)
                        
                else:
                    if current_psalm:
                        # For subsequent paragraphs, we normally don't expect a title repeats.
                        current_psalm['body_paragraphs'].append(full_text)
                        
    except Exception as e:
        print(f"Error extracting text: {e}")
        
    return psalms

# ------------------------------------------------------------------
# PDF GENERATION
# ------------------------------------------------------------------

def create_pdf(psalms_data, filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        leftMargin=OUTSIDE_MARGIN,
        rightMargin=OUTSIDE_MARGIN 
    )

    styles = getSampleStyleSheet()
    
    # 1. Header (PSALM X): 16pt bold, centered
    style_header = ParagraphStyle(
        'PsalmHeader',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=16,
        leading=18,
        alignment=TA_CENTER,
        keepWithNext=True
    )

    # 2. Subtitle (Title): 14pt italic, centered
    style_subtitle = ParagraphStyle(
        'PsalmSubtitle',
        parent=styles['Normal'],
        fontName='Times-Italic', 
        fontSize=14,
        leading=16,
        alignment=TA_CENTER,
        keepWithNext=True
    )

    # 3. Body: 12pt, Left Align, NO INDENT
    style_body = ParagraphStyle(
        'PsalmBody',
        parent=styles['BodyText'],
        fontName=FONT_NAME,
        fontSize=BODY_FONT_SIZE,
        leading=LEADING,
        alignment=TA_LEFT, # LEFT ALIGMENT FIXED
        firstLineIndent=0, # NO INDENT (Straight Edge)
        spaceAfter=6, 
        hyphenation=True,
        allowWidows=0,
        allowOrphans=0
    )
    
    # 4. Selah: italic, centered, 12pt before/after
    style_selah = ParagraphStyle(
        'Selah',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=BODY_FONT_SIZE,
        alignment=TA_CENTER,
        spaceBefore=12,
        spaceAfter=12
    )

    # Templates
    frame_w = PAGE_WIDTH - INSIDE_MARGIN - OUTSIDE_MARGIN
    frame_h = PAGE_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    
    frame_odd = Frame(INSIDE_MARGIN, BOTTOM_MARGIN, frame_w, frame_h, id='odd', showBoundary=0)
    template_odd = PageTemplate(id='Odd', frames=[frame_odd], onPage=lambda c,d: None)
    
    frame_even = Frame(OUTSIDE_MARGIN, BOTTOM_MARGIN, frame_w, frame_h, id='even', showBoundary=0)
    template_even = PageTemplate(id='Even', frames=[frame_even], onPage=lambda c,d: None)
    
    doc.addPageTemplates([template_odd, template_even])
    
    story = []
    
    # Pre-compiled regex for Selah
    # Matches "Selah" followed by optional punctuation/whitespace
    selah_pattern = re.compile(r'(Selah[\.\s]*)', re.IGNORECASE)
    
    for p in psalms_data:
        # Spacing: New Psalm = Big Gap
        if story:
             story.append(Spacer(1, 24)) 
        
        story.append(Paragraph(f"PSALM {p['number']}", style_header))
        story.append(Spacer(1, 12)) 
        
        if p['title']:
            story.append(Paragraph(p['title'], style_subtitle))
            story.append(Spacer(1, 18))
        else:
            story.append(Spacer(1, 12))
        
        # Additional cleaning for Body?
        # User said "Psalm 3... Subtitle appears twice".
        # If the duplicate wasn't at the very start of the extracted text (e.g. paragraph break),
        # We might need to check p['body_paragraphs'][0] specifically.
        
        # Check first paragraph for Title overlap if not already stripped
        # (The extraction logic above handles the case where Title is on SAME LINE as PSALM X)
        # But if Title is on NEXT LINE (New Paragraph), extraction logic above didn't see it.
        # Let's check here.
        
        body_paras = p['body_paragraphs']
        if body_paras and p['title']:
            # Check Clean version of Para 0 vs Title
            # Use stricter match to avoid accidents
            norm_p0 = normalize(body_paras[0])
            norm_title = normalize(p['title'])
            
            # If paragraph IS the title (short match)
            if norm_p0 == norm_title:
                # Remove this paragraph entirely
                body_paras.pop(0)
            elif norm_p0.startswith(norm_title) and len(norm_p0) < len(norm_title) + 10:
                # If it's title + small junk, remove
                body_paras.pop(0)

        for para_text in body_paras:
            # Split Selah
            parts = re.split(r'(Selah\.?)', para_text)
            for part in parts:
                if not part.strip():
                    continue
                if 'selah' in part.lower():
                     story.append(Paragraph(part.strip(), style_selah))
                else:
                     story.append(Paragraph(part.strip(), style_body))
            
    doc.build(story)
    print(f"PDF generated: {filename}")

if __name__ == "__main__":
    titles = get_psalm_titles(INPUT_XLSX)
    print(f"Loaded {len(titles)} titles.")
    
    psalms = extract_psalms(INPUT_DOCX, titles)
    print(f"Extracted {len(psalms)} Psalms.")
    
    if psalms:
        create_pdf(psalms, OUTPUT_FILENAME)
    else:
        print("No content found.")
