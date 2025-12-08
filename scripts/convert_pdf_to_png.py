import pymupdf
import pathlib

base_path = pathlib.Path("Creator/Usman Alex Kadiri")

for i in range(1, 13):
    pdf_name = f"Screenprint {i}.pdf"
    pdf_path = base_path / pdf_name
    
    if pdf_path.exists():
        print(f"Converting {pdf_name}...")
        try:
            doc = pymupdf.open(pdf_path)
            for page_num, page in enumerate(doc):
                pix = page.get_pixmap()
                output_name = f"Screenprint_{i}_page_{page_num}.png"
                pix.save(base_path / output_name)
                print(f"Saved {output_name}")
        except Exception as e:
            print(f"Error converting {pdf_name}: {e}")
    else:
        print(f"Warning: {pdf_name} not found.")
