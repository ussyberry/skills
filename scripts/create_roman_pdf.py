from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def int_to_roman(n):
    """
    Convert an integer to a Roman numeral.
    """
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while  n > 0:
        for _ in range(n // val[i]):
            roman_num += syb[i]
            n -= val[i]
        i += 1
    return roman_num

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Roman Numerals 1 to 1000")
    
    c.setFont("Helvetica", 12)
    y_position = height - 80
    column_width = 150
    x_positions = [50, 200, 350, 500] 
    
    current_column = 0
    items_per_column = 50 # Adjust as needed based on font size/spacing
    
    count = 0
    
    for i in range(1, 1001):
        roman = int_to_roman(i)
        text = f"{i}. {roman}"
        
        c.drawString(x_positions[current_column], y_position, text)
        y_position -= 15
        count += 1
        
        # Move to next column if near bottom
        if y_position < 50:
            y_position = height - 80
            current_column += 1
            
            # New page if columns full
            if current_column >= len(x_positions):
                c.showPage()
                # Reset for new page
                c.setFont("Helvetica", 12)
                y_position = height - 80
                current_column = 0

    c.save()
    print(f"PDF created successfully: {filename}")

if __name__ == "__main__":
    output_file = "roman_numerals.pdf"
    create_pdf(output_file)
