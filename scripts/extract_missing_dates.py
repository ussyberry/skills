from pypdf import PdfReader
import pathlib

# Path to the resume PDF
resume_path = pathlib.Path("Creator/Usman Alex Kadiri/USMAN ALEX KADIRI RESUME 0425.pdf")
output_file = pathlib.Path("extracted_resume_text_raw.txt")

if resume_path.exists():
    print(f"Extracting text from {resume_path}...")
    try:
        reader = PdfReader(str(resume_path))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n--------------------------------------------------\n"
        
        output_file.write_text(text, encoding="utf-8")
        print(f"Saved raw text extraction to {output_file}")
    except Exception as e:
        print(f"Error extracting text: {e}")
else:
    print(f"Error: {resume_path} not found.")
