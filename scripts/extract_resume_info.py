import pymupdf4llm
import pathlib

resume_pdf = pathlib.Path("Creator/Usman Alex Kadiri/USMAN ALEX KADIRI RESUME 0425.pdf")
education_pdf = pathlib.Path("Creator/Usman Alex Kadiri/Usman Kadiri Education.pdf")


output_file = pathlib.Path("extracted_info.md")
content = []
content.append(f"--- EXTRACTING: {resume_pdf.name} ---")
content.append(pymupdf4llm.to_markdown(str(resume_pdf)))
content.append("\n" + "="*50 + "\n")
content.append(f"--- EXTRACTING: {education_pdf.name} ---")
content.append(pymupdf4llm.to_markdown(str(education_pdf)))

output_file.write_text("\n".join(content), encoding="utf-8")
print("Extraction complete.")
