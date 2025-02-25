import pytesseract
from PIL import Image
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pages = convert_from_path('your_pdf.pdf', 300)
text = ""

for page in pages:
    text += pytesseract.image_to_string(page)

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(text)
