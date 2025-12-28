#!/usr/bin/env python3
"""
Generate a professional Canadian-standard resume PDF for Microsoft Solution Area Specialist role.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Resume content tailored for Microsoft Solution Area Specialist role
RESUME_DATA = {
    "header": {
        "name": "USMAN ALEX KADIRI",
        "phone": "613-404-5024",
        "email": "lexus.kadiri@gmail.com",
        "location": "Ottawa, Ontario, K1V 9N6",
        "linkedin": "linkedin.com/in/usman-alex-kadiri-ctc-4495026a/"
    },
    "summary": (
        "Experienced public sector professional with extensive background in government operations, "
        "finance, customer service, and data management. Demonstrated ability to excel in fast-paced "
        "environments, resolve complex issues, and deliver high-quality service. Skilled in business "
        "planning, analytics, Microsoft Office, and stakeholder communications. Holds Government of "
        "Canada Reliability Security Clearance, a Master's degree in Finance, and a B.Sc. in Economics. "
        "Actively pursuing advanced certifications in AI, Data Science, and Digital Transformation to "
        "drive business value in technology solutions."
    ),
    "core_competencies": {
        "Public Sector & Government Operations": [
            "Federal government operations and compliance",
            "Government of Canada Reliability Security Clearance (Current)",
            "Understanding of regulatory frameworks and budget cycles",
            "Public sector stakeholder management"
        ],
        "Data Analytics & Business Intelligence": [
            "Data entry and management systems",
            "Business planning and analytics",
            "Financial analysis and modeling",
            "Statistical analysis and reporting"
        ],
        "CRM & Technology Platforms": [
            "Microsoft Office Suite (Word, Excel, PowerPoint, Outlook)",
            "CRM platforms and telephony systems",
            "Data integrity and confidentiality management",
            "Technical support and troubleshooting"
        ],
        "Communication & Stakeholder Management": [
            "Stakeholder relationship building",
            "Negotiation and conflict resolution",
            "Cross-functional collaboration",
            "Professional communication and presentation"
        ],
        "Digital Transformation & AI": [
            "Artificial Intelligence foundations",
            "Generative AI applications",
            "Data Science and Machine Learning",
            "Digital transformation concepts"
        ],
        "Security & Compliance": [
            "Government of Canada Reliability Security Clearance (Current)",
            "Data privacy and confidentiality",
            "Regulatory compliance",
            "Security awareness and best practices"
        ]
    },
    "experience": [
        {
            "title": "Call Centre Agent – Debt Management Call Centre (DMCC)",
            "company": "Canada Revenue Agency, Ottawa",
            "period": "January 2023 – Present",
            "achievements": [
                "Conduct taxpayer interviews to verify financial information per CRA policies",
                "Negotiate payment arrangements and collect tax debts per federal guidelines",
                "Respond to inquiries about system letters and collection processes",
                "Request missing tax returns and follow up on overdue accounts",
                "Update taxpayer contact info ensuring data integrity and confidentiality",
                "Refer complex cases to senior staff or specialized teams",
                "Meet performance targets in high-volume, fast-paced environment",
                "Maintain Government of Canada Reliability Security Clearance"
            ]
        },
        {
            "title": "Corporate Travel Counselor",
            "company": "American Express Global Business Travel, Ottawa",
            "period": "September 2021 – November 2022",
            "achievements": [
                "Assist customers with travel bookings and resolve inquiries",
                "Utilize telephony systems and booking platforms for service delivery",
                "Provide technical support, troubleshooting, and escalation handling",
                "Manage flight exchanges, refunds, and schedule changes"
            ]
        },
        {
            "title": "Data Entry & Verification Clerk (Casual)",
            "company": "City of Ottawa",
            "period": "March 2021 – February 2022",
            "achievements": [
                "Perform accurate data entry of confidential health information",
                "Verify and maintain data integrity in databases and spreadsheets",
                "Ensure compliance with data privacy and confidentiality requirements"
            ]
        },
        {
            "title": "Call Centre Agent (TD Inbound English)",
            "company": "Millennium 1 Solutions, Ottawa",
            "period": "March 2021 – June 2021",
            "achievements": [
                "Handle inbound calls for TD Wealth and TD Direct Investing clients",
                "Authenticate clients, document call details, report security incidents",
                "Maintain high standards of customer service and security compliance"
            ]
        },
        {
            "title": "Quotations & Listing Specialist",
            "company": "The Nigerian Stock Exchange, Abuja",
            "period": "October 2016 – January 2021",
            "achievements": [
                "Develop and maintain relationships with listed companies",
                "Conduct post-listing visits and generate analytical reports",
                "Represent the Exchange at statutory meetings",
                "Contribute to business development and stakeholder engagement"
            ]
        },
        {
            "title": "Branch Manager",
            "company": "The Nigerian Stock Exchange, Kano",
            "period": "October 2010 – October 2016",
            "achievements": [
                "Supervise branch operations ensuring compliance and record-keeping",
                "Serve as co-signatory to bank accounts and organize financial literacy programs",
                "Manage team performance and operational excellence"
            ]
        },
        {
            "title": "Branch Administration Officer",
            "company": "The Nigerian Stock Exchange, Abuja",
            "period": "January 2008 – October 2010",
            "achievements": [
                "Provide technical and administrative support for trading floor operations",
                "Maintain IT infrastructure and ensure regular asset maintenance",
                "Support operational efficiency and system reliability"
            ]
        }
    ],
    "education": [
        {
            "degree": "Master of Science (MSc) in Finance",
            "institution": "Leeds Beckett University, United Kingdom",
            "period": "2004",
            "details": "Canadian Equivalency verified as Master's degree by WES (August 2019)"
        },
        {
            "degree": "Bachelor of Science (B.Sc.) in Economics",
            "institution": "University of Abuja, Nigeria",
            "period": "January 1996 – September 2000",
            "details": ""
        }
    ],
    "certifications": [
        {
            "name": "Oracle Cloud Infrastructure 2025 Certified AI Foundations Associate",
            "issuer": "Oracle",
            "year": "2025"
        },
        {
            "name": "Oracle Cloud Infrastructure 2025 Certified Generative AI Professional",
            "issuer": "Oracle",
            "year": "2025"
        },
        {
            "name": "Discover Artificial Intelligence",
            "issuer": "Canada School of Public Service",
            "year": "2025"
        },
        {
            "name": "Discover Cyber Security",
            "issuer": "Canada School of Public Service",
            "year": "2025"
        },
        {
            "name": "Using Generative AI in the Government of Canada",
            "issuer": "Canada School of Public Service",
            "year": "2023"
        },
        {
            "name": "How Blockchain Technology is Transforming Businesses",
            "issuer": "Canada School of Public Service",
            "year": "2023"
        },
        {
            "name": "Access to Information and Privacy Fundamentals",
            "issuer": "Canada School of Public Service",
            "year": "2023"
        },
        {
            "name": "Security Awareness (Canada)",
            "issuer": "Canada School of Public Service",
            "year": "2023"
        },
        {
            "name": "Become a Data Scientist",
            "issuer": "LinkedIn Learning",
            "year": "2020"
        },
        {
            "name": "Data Science Analytics Career Paths & Certifications",
            "issuer": "LinkedIn Learning",
            "year": "2020"
        },
        {
            "name": "Data Visualization: Storytelling",
            "issuer": "LinkedIn Learning",
            "year": "2020"
        },
        {
            "name": "Excel 2016: Managing and Analyzing Data",
            "issuer": "LinkedIn Learning",
            "year": "2020"
        },
        {
            "name": "Learning Data Governance",
            "issuer": "LinkedIn Learning",
            "year": "2020"
        },
        {
            "name": "Statistics Foundations 1",
            "issuer": "LinkedIn Learning",
            "year": "2020"
        },
        {
            "name": "The Data Science of Economics, Banking, and Finance",
            "issuer": "LinkedIn Learning",
            "year": "2020"
        },
        {
            "name": "Artificial Intelligence for Project Managers",
            "issuer": "LinkedIn Learning",
            "year": "2020"
        },
        {
            "name": "Introducing AI to Your Organization",
            "issuer": "LinkedIn Learning",
            "year": "2020"
        },
        {
            "name": "DFIN-511: Introduction to Digital Currencies",
            "issuer": "University of Nicosia",
            "year": "2020"
        },
        {
            "name": "Data Science Orientation",
            "issuer": "Coursera",
            "year": "2019"
        },
        {
            "name": "Digital Skills: Artificial Intelligence",
            "issuer": "Accenture",
            "year": "2019"
        },
        {
            "name": "Introduction to Data Science",
            "issuer": "Cognitive Class",
            "year": "2019"
        },
        {
            "name": "What is Data Science?",
            "issuer": "IBM",
            "year": "2019"
        },
        {
            "name": "Business Development Foundations",
            "issuer": "LinkedIn Learning",
            "year": "2019"
        },
        {
            "name": "Fundamentals of Project Management",
            "issuer": "University of California, Berkeley",
            "year": "2019"
        },
        {
            "name": "Introduction to Anti-Corruption",
            "issuer": "UNODC",
            "year": "2019"
        },
        {
            "name": "Excel 2016: Business Process Analysis",
            "issuer": "LinkedIn Learning",
            "year": "2019"
        },
        {
            "name": "Excel for Corporate Finance Professionals",
            "issuer": "LinkedIn Learning",
            "year": "2019"
        },
        {
            "name": "Financial Modeling Foundations",
            "issuer": "LinkedIn Learning",
            "year": "2019"
        },
        {
            "name": "Financial Analysis: Introduction to Business Performance Analysis",
            "issuer": "LinkedIn Learning",
            "year": "2019"
        }
    ],
    "security_clearance": "Government of Canada Reliability Security Clearance (Current)"
}


def create_resume_pdf(output_path):
    """Create a professional resume PDF using ReportLab."""
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        name='HeaderName',
        parent=styles['Heading1'],
        fontSize=18,
        fontName='Helvetica-Bold',
        spaceAfter=6,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1a1a1a')
    ))
    
    styles.add(ParagraphStyle(
        name='HeaderContact',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica',
        alignment=TA_CENTER,
        spaceAfter=12,
        textColor=colors.HexColor('#4a4a4a')
    ))
    
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=12,
        fontName='Helvetica-Bold',
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.HexColor('#0066cc'),
        borderWidth=2,
        borderColor=colors.HexColor('#0066cc'),
        borderPadding=(0, 0, 0, 0)
    ))
    
    styles.add(ParagraphStyle(
        name='JobTitle',
        parent=styles['Heading3'],
        fontSize=11,
        fontName='Helvetica-Bold',
        spaceBefore=8,
        spaceAfter=2,
        textColor=colors.HexColor('#1a1a1a')
    ))
    
    styles.add(ParagraphStyle(
        name='CompanyInfo',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica-Oblique',
        spaceAfter=4,
        textColor=colors.HexColor('#4a4a4a')
    ))
    
    styles.add(ParagraphStyle(
        name='BulletPoint',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica',
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=2,
        textColor=colors.HexColor('#333333')
    ))
    
    styles.add(ParagraphStyle(
        name='Summary',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica',
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#333333')
    ))
    
    styles.add(ParagraphStyle(
        name='CompetencyCategory',
        parent=styles['Heading4'],
        fontSize=10,
        fontName='Helvetica-Bold',
        spaceBefore=6,
        spaceAfter=2,
        textColor=colors.HexColor('#0066cc')
    ))
    
    styles.add(ParagraphStyle(
        name='CompetencyItem',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica',
        leftIndent=10,
        spaceAfter=1,
        textColor=colors.HexColor('#333333')
    ))
    
    styles.add(ParagraphStyle(
        name='EducationItem',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica',
        spaceAfter=6,
        textColor=colors.HexColor('#333333')
    ))
    
    styles.add(ParagraphStyle(
        name='CertificationItem',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica',
        spaceAfter=2,
        textColor=colors.HexColor('#333333')
    ))
    
    styles.add(ParagraphStyle(
        name='SecurityClearance',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica-Bold',
        spaceBefore=10,
        spaceAfter=6,
        textColor=colors.HexColor('#0066cc')
    ))
    
    # Build the content
    content = []
    
    # Header
    content.append(Paragraph(RESUME_DATA["header"]["name"], styles['HeaderName']))
    
    contact_info = (
        f"{RESUME_DATA['header']['phone']} | {RESUME_DATA['header']['email']} | "
        f"{RESUME_DATA['header']['location']} | {RESUME_DATA['header']['linkedin']}"
    )
    content.append(Paragraph(contact_info, styles['HeaderContact']))
    content.append(Spacer(1, 0.1*inch))
    
    # Professional Summary
    content.append(Paragraph("PROFESSIONAL SUMMARY", styles['SectionHeader']))
    content.append(Paragraph(RESUME_DATA["summary"], styles['Summary']))
    
    # Professional Experience
    content.append(Paragraph("PROFESSIONAL EXPERIENCE", styles['SectionHeader']))
    
    for exp in RESUME_DATA["experience"]:
        content.append(Paragraph(exp["title"], styles['JobTitle']))
        content.append(Paragraph(f"{exp['company']} | {exp['period']}", styles['CompanyInfo']))
        
        for achievement in exp["achievements"]:
            content.append(Paragraph(f"• {achievement}", styles['BulletPoint']))
        
        content.append(Spacer(1, 0.05*inch))
    
    # Education
    content.append(Paragraph("EDUCATION", styles['SectionHeader']))
    
    for edu in RESUME_DATA["education"]:
        edu_text = f"<b>{edu['degree']}</b> | {edu['institution']} | {edu['period']}"
        if edu['details']:
            edu_text += f"<br/><i>{edu['details']}</i>"
        content.append(Paragraph(edu_text, styles['EducationItem']))
    
    content.append(Spacer(1, 0.1*inch))
    
    # Certifications (Selected - most relevant)
    content.append(Paragraph("CERTIFICATIONS", styles['SectionHeader']))
    
    # Show most relevant certifications first
    relevant_certs = RESUME_DATA["certifications"][:15]  # First 15 are most recent/relevant
    
    for cert in relevant_certs:
        cert_text = f"<b>{cert['name']}</b> - {cert['issuer']} ({cert['year']})"
        content.append(Paragraph(cert_text, styles['CertificationItem']))
    
    content.append(Spacer(1, 0.1*inch))
    
    # Security Clearance (Prominently featured)
    content.append(Paragraph("SECURITY CLEARANCE", styles['SectionHeader']))
    content.append(Paragraph(RESUME_DATA["security_clearance"], styles['SecurityClearance']))
    
    # Core Competencies (moved to end) - 3 sets of 2 columns
    content.append(Paragraph("CORE COMPETENCIES", styles['SectionHeader']))
    
    # Create a table for competencies - 3 sets of 2 columns
    competency_data = []
    categories = list(RESUME_DATA["core_competencies"].keys())
    
    # Set 1: Categories 1 & 2
    competency_data.append([Paragraph(f"<b>{categories[0]}</b>", styles['CompetencyCategory']),
                           Paragraph(f"<b>{categories[1]}</b>", styles['CompetencyCategory'])])
    for i in range(4):
        row = []
        for cat_idx in [0, 1]:
            if i < len(RESUME_DATA["core_competencies"][categories[cat_idx]]):
                row.append(Paragraph(f"• {RESUME_DATA['core_competencies'][categories[cat_idx]][i]}", styles['CompetencyItem']))
            else:
                row.append(Paragraph("", styles['CompetencyItem']))
        competency_data.append(row)
    
    # Set 2: Categories 3 & 4
    competency_data.append([Paragraph(f"<b>{categories[2]}</b>", styles['CompetencyCategory']),
                           Paragraph(f"<b>{categories[3]}</b>", styles['CompetencyCategory'])])
    for i in range(4):
        row = []
        for cat_idx in [2, 3]:
            if i < len(RESUME_DATA["core_competencies"][categories[cat_idx]]):
                row.append(Paragraph(f"• {RESUME_DATA['core_competencies'][categories[cat_idx]][i]}", styles['CompetencyItem']))
            else:
                row.append(Paragraph("", styles['CompetencyItem']))
        competency_data.append(row)
    
    # Set 3: Categories 5 & 6
    competency_data.append([Paragraph(f"<b>{categories[4]}</b>", styles['CompetencyCategory']),
                           Paragraph(f"<b>{categories[5]}</b>", styles['CompetencyCategory'])])
    for i in range(4):
        row = []
        for cat_idx in [4, 5]:
            if i < len(RESUME_DATA["core_competencies"][categories[cat_idx]]):
                row.append(Paragraph(f"• {RESUME_DATA['core_competencies'][categories[cat_idx]][i]}", styles['CompetencyItem']))
            else:
                row.append(Paragraph("", styles['CompetencyItem']))
        competency_data.append(row)
    
    competency_table = Table(competency_data, colWidths=[2.5*inch, 2.5*inch])
    competency_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    content.append(competency_table)
    
    # Build the PDF
    doc.build(content)
    print(f"Resume PDF created successfully: {output_path}")


if __name__ == "__main__":
    # Create output directory if it doesn't exist
    output_dir = "Creator"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate the resume
    output_path = os.path.join(output_dir, "Usman_Alex_Kadiri_Microsoft_Solution_Specialist_Resume.pdf")
    create_resume_pdf(output_path)
