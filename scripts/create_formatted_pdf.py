from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
import pathlib
import sys
import re

# Define paths
md_path = pathlib.Path("Creator/resume.md")
pdf_path = pathlib.Path("Creator/Usman_Alex_Kadiri_Resume.pdf")

def create_resume_pdf(md_file, pdf_file):
    print(f"Reading {md_file}...", flush=True)
    try:
        text = md_file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file: {e}", flush=True)
        return
    
    doc = SimpleDocTemplate(str(pdf_file), pagesize=letter,
                            rightMargin=50, leftMargin=50,
                            topMargin=50, bottomMargin=50)
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    styles.add(ParagraphStyle(name='ResumeTitle', parent=styles['Heading1'], fontSize=24, spaceAfter=20, alignment=TA_LEFT, textColor=colors.darkblue))
    styles.add(ParagraphStyle(name='ResumeH1', parent=styles['Heading2'], fontSize=16, spaceBefore=15, spaceAfter=10, textColor=colors.darkblue, borderPadding=5, borderColor=colors.lightgrey, borderWidth=0, borderBottomWidth=1))
    styles.add(ParagraphStyle(name='ResumeH2', parent=styles['Heading3'], fontSize=12, spaceBefore=10, spaceAfter=5, textColor=colors.black, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='ResumeBody', parent=styles['Normal'], fontSize=10, spaceAfter=6, leading=14))
    styles.add(ParagraphStyle(name='ResumeBullet', parent=styles['Normal'], fontSize=10, leading=14, leftIndent=15, bulletIndent=0))

    story = []
    
    lines = text.split('\n')

    def format_inline(text):
        # Bold
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        # Italic
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        # Links
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" color="blue">\1</a>', text)
        return text

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Headers
        if line.startswith('# '):
            header_text = line[2:].strip()
            story.append(Paragraph(format_inline(header_text), styles['ResumeTitle']))
        elif line.startswith('## '):
            header_text = line[3:].strip()
            story.append(Paragraph(format_inline(header_text), styles['ResumeH1']))
        elif line.startswith('### '):
            header_text = line[4:].strip()
            story.append(Paragraph(format_inline(header_text), styles['ResumeH2']))
        
        # Lists
        elif line.startswith('- '):
            list_text = line[2:].strip()
            # Use bulletChar for simple bullets
            story.append(Paragraph(format_inline(list_text), styles['ResumeBullet'], bulletText='•'))
        
        # Normal Text
        else:
            story.append(Paragraph(format_inline(line), styles['ResumeBody']))

    print(f"Generating PDF at {pdf_file}...", flush=True)
    try:
        doc.build(story)
        print("PDF generation complete!", flush=True)
    except Exception as e:
        print(f"Error building PDF: {e}", flush=True)

if __name__ == "__main__":
    create_resume_pdf(md_path, pdf_path)
