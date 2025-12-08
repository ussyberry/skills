import pymupdf4llm
import pathlib
import re

base_path = pathlib.Path("Creator/Usman Alex Kadiri")
output_file = pathlib.Path("extracted_certifications.md")

content = []

def clean_text(text):
    # Remove excessive newlines and headers usually found in prints
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        line = line.strip()
        if line and "Licenses & certifications" not in line and "Page" not in line:
            cleaned.append(line)
    return "\n".join(cleaned)

for i in range(1, 13):
    pdf_name = f"Screenprint {i}.pdf"
    pdf_path = base_path / pdf_name
    
    if pdf_path.exists():
        print(f"Extracting {pdf_name}...")
        try:
            text = pymupdf4llm.to_markdown(str(pdf_path))
            content.append(f"## {pdf_name}\n")
            content.append(clean_text(text))
            content.append("\n" + "-"*30 + "\n")
        except Exception as e:
            content.append(f"## {pdf_name} - ERROR: {e}\n")
    else:
        print(f"Warning: {pdf_name} not found.")

output_file.write_text("\n".join(content), encoding="utf-8")
print(f"Saved extraction to {output_file}")
