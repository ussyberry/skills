from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib import colors
import pathlib
import sys
import re

# Define paths
md_path = pathlib.Path("Creator/resume_data_scientist.md")
pdf_path = pathlib.Path("Creator/Usman_Alex_Kadiri_Data_Scientist_Resume.pdf")

# Colors
PRIMARY_COLOR = colors.HexColor("#0f2c4c") # Dark Navy Blue
ACCENT_COLOR = colors.HexColor("#2C3E50") # Slate Blue/Grey
TEXT_COLOR = colors.HexColor("#333333")    # Dark Grey
LIGHT_GREY = colors.HexColor("#f4f4f4")    # Very Light Grey for backgrounds

def create_ds_resume(md_file, pdf_file):
    print(f"Reading {md_file}...", flush=True)
    try:
        text = md_file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file: {e}", flush=True)
        return
    
    doc = SimpleDocTemplate(str(pdf_file), pagesize=letter,
                            rightMargin=40, leftMargin=40,
                            topMargin=40, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    styles.add(ParagraphStyle(name='R_Title', parent=styles['Heading1'], fontSize=28, alignment=TA_CENTER, textColor=PRIMARY_COLOR, fontName='Helvetica-Bold', spaceAfter=6))
    styles.add(ParagraphStyle(name='R_Subtitle', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER, textColor=ACCENT_COLOR, fontName='Helvetica-Oblique', spaceAfter=12))
    styles.add(ParagraphStyle(name='R_Contact', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=TEXT_COLOR))
    
    styles.add(ParagraphStyle(name='Col_Header', parent=styles['Heading3'], fontSize=12, textColor=PRIMARY_COLOR, fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=6, borderPadding=2, borderColor=colors.lightgrey, borderWidth=0, borderBottomWidth=1))
    styles.add(ParagraphStyle(name='Body_Text', parent=styles['Normal'], fontSize=9, leading=13, textColor=TEXT_COLOR, spaceAfter=6))
    styles.add(ParagraphStyle(name='Job_Title', parent=styles['Normal'], fontSize=10, leading=13, textColor=colors.black, fontName='Helvetica-Bold', spaceBefore=8))
    styles.add(ParagraphStyle(name='Job_Meta', parent=styles['Normal'], fontSize=9, leading=13, textColor=ACCENT_COLOR, fontName='Helvetica-Oblique'))
    styles.add(ParagraphStyle(name='Skill_Item', parent=styles['Normal'], fontSize=9, leading=12, textColor=TEXT_COLOR, spaceAfter=3))
    
    # Parsing
    sections = {
        'Header': [],
        'Summary': [],
        'Skills': [],
        'Experience': [],
        'Education': [],
        'Certifications': []
    }
    
    current_section = 'Header'
    lines = text.split('\n')
    
    def format_inline(text):
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" color="#0000EE">\1</a>', text)
        return text

    # Simple parser to categorize content
    # NOTE: This parsing logic is tailored to the specific structure of resume_data_scientist.md
    for line in lines:
        line = line.strip()
        if not line: continue
        
        if line.startswith('## Professional Summary'):
            current_section = 'Summary'
        elif line.startswith('## Core Skills'):
            current_section = 'Skills'
        elif line.startswith('## Experience'):
            current_section = 'Experience'
        elif line.startswith('## Education'):
            current_section = 'Education'
        elif line.startswith('## Key Certifications'):
            current_section = 'Certifications'
        elif line.startswith('# Usman'): # Name already handled in specific logic below if needed, but mostly lines
            pass 
        else:
            # Content
            if current_section == 'Header':
                if line.startswith('# '):
                   sections['Header'].append(Paragraph(format_inline(line[2:]), styles['R_Title']))
                elif line.startswith('**') and 'Professional' in line:
                    clean = line.replace('**', '')
                    sections['Header'].append(Paragraph(format_inline(clean), styles['R_Subtitle']))
                elif line.startswith('*'):
                     sections['Header'].append(Paragraph(format_inline(line), styles['R_Subtitle']))
                else:
                    sections['Header'].append(Paragraph(format_inline(line), styles['R_Contact']))
            
            elif current_section == 'Summary':
                 sections['Summary'].append(Paragraph(format_inline(line), styles['Body_Text']))

            elif current_section == 'Skills':
                if line.startswith('**'):
                    sections['Skills'].append(Spacer(1, 4))
                    sections['Skills'].append(Paragraph(format_inline(line), styles['Body_Text']))
                elif not line.startswith('- '): # Description lines
                    sections['Skills'].append(Paragraph(format_inline(line), styles['Skill_Item']))

            elif current_section == 'Experience':
                if line.startswith('### '):
                    # Company
                    pass # We might just treat company as part of job block
                elif line.startswith('**'):
                    # Job Title | Dates
                    parts = line.split('|')
                    title = parts[0].strip().replace('**', '')
                    date = parts[1].strip() if len(parts) > 1 else ""
                    sections['Experience'].append(Paragraph(f"<b>{title}</b>", styles['Job_Title']))
                    if date:
                         sections['Experience'].append(Paragraph(date, styles['Job_Meta']))
                elif not line.startswith('- '):
                     # Company Name line (usually simple bold in md, but here likely Just text)
                     # For this specific MD, Companies are ### headers.
                     # Let's handle generic lines
                     sections['Experience'].append(Paragraph(format_inline(line), styles['Job_Meta'])) # Company name usually
                elif line.startswith('- '):
                     sections['Experience'].append(Paragraph(f"• {format_inline(line[2:])}", styles['Body_Text']))

            elif current_section in ['Education', 'Certifications']:
                 if line.startswith('**'):
                     sections[current_section].append(Spacer(1, 4))
                     sections[current_section].append(Paragraph(format_inline(line), styles['Body_Text'])) # Title
                 elif line.startswith('- '):
                      sections[current_section].append(Paragraph(f"• {format_inline(line[2:])}", styles['Skill_Item']))
                 else:
                      sections[current_section].append(Paragraph(format_inline(line), styles['Skill_Item']))
    
    
    # --- Layout Assembly ---
    story = []
    
    # 1. Header (Full Width)
    for elem in sections['Header']:
        story.append(elem)
    story.append(Spacer(1, 20))
    story.append(Paragraph("", ParagraphStyle('Line', borderBottomWidth=1, borderColor=PRIMARY_COLOR, spaceAfter=20)))

    # 2. Main Content (2 Columns) - Multi-Row Table Strategy
    
    # Prepare chunks for Left Column
    left_chunks = []
    
    # Left Chunk 1: Education
    l_edu = [Paragraph("Education", styles['Col_Header'])] + sections['Education'] + [Spacer(1, 12)]
    left_chunks.append(l_edu)
    
    # Left Chunk 2: Skills
    l_skills = [Paragraph("Core Skills", styles['Col_Header'])] + sections['Skills'] + [Spacer(1, 12)]
    left_chunks.append(l_skills)
    
    # Left Chunk 3: Certifications Start
    # We will split Certifications into multiple smaller chunks to balance with Right Column rows
    certs_header = [Paragraph("Certifications", styles['Col_Header'])]
    certs_items = sections['Certifications']
    
    # Chunk size for certs (e.g. 5 items per chunk)
    CERT_CHUNK_SIZE = 5
    cert_chunks = []
    
    # First chunk includes header
    first_cert_chunk = certs_header + certs_items[:CERT_CHUNK_SIZE] + [Spacer(1, 12)]
    cert_chunks.append(first_cert_chunk)
    
    # Remaining chunks
    for i in range(CERT_CHUNK_SIZE, len(certs_items), CERT_CHUNK_SIZE):
        chunk = certs_items[i:i+CERT_CHUNK_SIZE] + [Spacer(1, 12)]
        cert_chunks.append(chunk)

    left_chunks.append(cert_chunks[0])
    for c in cert_chunks[1:]:
        left_chunks.append(c)

    # Prepare chunks for Right Column
    right_chunks = []
    
    # Right Chunk 1: Summary
    r_summary = [Paragraph("Professional Summary", styles['Col_Header'])] + sections['Summary'] + [Spacer(1, 12)]
    right_chunks.append(r_summary)
    
    # Right Chunks 2+: Experience Items
    # We need to parse experience section into distinct jobs to create separate chunks
    # Re-parsing Experience logic into chunks
    current_job = []
    
    # Add Header first
    current_job.append(Paragraph("Professional Experience", styles['Col_Header']))

    in_exp = False
    for line in lines:
        if line.startswith('## Experience'): in_exp = True; continue
        if line.startswith('## ') and not line.startswith('## Experience'): in_exp = False
        
        if in_exp and line.strip():
            if line.startswith('### '):
                # New Job -> Save previous chunk if exists (and not just header)
                if len(current_job) > 1: # >1 because header might be there
                    # Check if it's just header
                    if len(current_job) == 1 and current_job[0].text == "Professional Experience":
                         pass # Just keep collecting
                    else:
                         right_chunks.append(current_job)
                         current_job = [] # Start new
                
                # Company
                company = line[3:].strip()
                current_job.append(Spacer(1, 4)) # Reduced from 8
                current_job.append(Paragraph(f"{company}", styles['Job_Meta']))
            elif line.startswith('**'):
                # Title
                parts = line.split('|')
                title = parts[0].strip().replace('**', '')
                date = parts[1].strip().replace('*', '') if len(parts) > 1 else ""
                
                if title.strip(): # Only add title line if text exists
                    current_job.append(Paragraph(f"<b>{title}</b>", styles['Job_Title']))
                
                if date:
                    # If title was empty, we might want the date on the same line or just below company? 
                    # For now, standard body text style for date is fine, maybe slightly different if standalone
                    style_to_use = styles['Body_Text'] if title.strip() else styles['Job_Meta']
                    current_job.append(Paragraph(f"<font color='grey'>{date}</font>", style_to_use)) 
            elif line.startswith('- '):
                 current_job.append(Paragraph(f"• {format_inline(line[2:])}", styles['Body_Text']))
    
    # Append final job
    if current_job:
        right_chunks.append(current_job)

    # Balance Rows
    rows_data = []
    max_rows = max(len(left_chunks), len(right_chunks))
    
    for i in range(max_rows):
        left_cell = left_chunks[i] if i < len(left_chunks) else []
        right_cell = right_chunks[i] if i < len(right_chunks) else []
        rows_data.append([left_cell, right_cell])
        
    # Create Table
    col_widths = [160, 372] 
    
    t = Table(rows_data, colWidths=col_widths, splitByRow=1)
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (0,-1), 0),
        ('RIGHTPADDING', (0,0), (0,-1), 10),
        ('LEFTPADDING', (1,0), (1,-1), 10),
        ('RIGHTPADDING', (1,0), (1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LINEAFTER', (0,0), (0,-1), 0.5, colors.lightgrey), # Vertical divider behavior might be tricky with row split, but let's try
    ]))
    
    story.append(t)
    
    print(f"Generating PDF at {pdf_file}...", flush=True)
    try:
        doc.build(story)
        print("PDF generation complete!", flush=True)
    except Exception as e:
        print(f"Error building PDF: {e}", flush=True)

if __name__ == "__main__":
    create_ds_resume(md_path, pdf_path)
