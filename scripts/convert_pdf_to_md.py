import pymupdf4llm
import pathlib

# Define paths
pdf_path = pathlib.Path("PDFs/roman_numerals.pdf")
md_path = pathlib.Path("roman_numerals.md")

print(f"Converting {pdf_path} to Markdown...")

# Convert to markdown
md_text = pymupdf4llm.to_markdown(str(pdf_path))

# Save to file
md_path.write_text(md_text, encoding="utf-8")

print(f"Conversion complete! Saved to {md_path}")
