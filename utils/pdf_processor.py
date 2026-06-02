from PyPDF2 import PdfReader
import pytesseract
from pdf2image import convert_from_path

# Update this path if Tesseract is installed elsewhere
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text(pdf_path):

    reader = PdfReader(pdf_path)

    pages = []

    for i, page in enumerate(reader.pages):

        text = page.extract_text()

        # OCR fallback for scanned PDFs
        if not text or text.strip() == "":

            try:

                images = convert_from_path(
                    pdf_path,
                    first_page=i + 1,
                    last_page=i + 1
                )

                text = pytesseract.image_to_string(
                    images[0]
                )

            except Exception as e:

                print(
                    f"OCR failed on page {i + 1}: {e}"
                )

                text = ""

        pages.append({

            "page": i + 1,

            "text": text

        })

    return pages