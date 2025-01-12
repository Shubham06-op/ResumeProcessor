import re
from PyPDF2 import PdfReader
from docx import Document

def extract_info_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return extract_info_from_text(text)

def extract_info_from_docx(file_path):
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return extract_info_from_text(text)

def extract_info_from_text(text):
    name_pattern = r'\b[A-Z][a-z]*\s[A-Z][a-z]*\b'  # Example: John Doe
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    phone_pattern = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'

    first_name = re.search(name_pattern, text)
    email = re.search(email_pattern, text)
    mobile_number = re.search(phone_pattern, text)

    return {
        'first_name': first_name.group() if first_name else 'Not Found',
        'email': email.group() if email else 'Not Found',
        'mobile_number': mobile_number.group() if mobile_number else 'Not Found',
    }
