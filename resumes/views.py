import re
import docx
import PyPDF2
import logging
from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response

logging.basicConfig(level=logging.DEBUG)

class ResumeExtractView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        resume_file = request.FILES.get('resume')
        
        if resume_file:
            resume_text = self.extract_text_from_resume(resume_file)
            
            first_name = self.extract_first_name(resume_text)
            email = self.extract_email(resume_text)
            mobile_number = self.extract_mobile_number(resume_text)

            data = {
                'first_name': first_name,
                'email': email,
                'mobile_number': mobile_number,
            }
            return Response(data)

        return Response({"error": "No resume file uploaded"}, status=400)

    def extract_text_from_resume(self, file):
        file_extension = file.name.split('.')[-1].lower()
        if file_extension == 'pdf':
            return self.extract_text_from_pdf(file)
        elif file_extension in ['doc', 'docx']:
            return self.extract_text_from_docx(file)
        else:
            return ""

    def extract_text_from_pdf(self, file):
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        logging.debug("Extracted text from PDF: %s", text[:500])  # Log part of the text
        return text

    def extract_text_from_docx(self, file):
        doc = docx.Document(file)
        text = ''
        for para in doc.paragraphs:
            text += para.text
        logging.debug("Extracted text from DOCX: %s", text[:500])  # Log part of the text
        return text

    def extract_first_name(self, text):
        lines = text.split('\n')
        name_line = lines[0] if lines else ""
        name_parts = name_line.split()
        first_name = name_parts[0] if name_parts else ""
        logging.debug("Extracted first name: %s", first_name)
        return first_name

    def extract_email(self, text):
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
        email = email_match.group(0) if email_match else ""
        logging.debug("Extracted email: %s", email)
        return email

    def extract_mobile_number(self, text):
        phone_match = re.search(
            r'(?:\+?\d{1,4}[-.\s]?)?(?:\(?\d{1,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{4}', 
            text
        )
        phone_number = phone_match.group(0) if phone_match else ""
        logging.debug("Extracted phone number: %s", phone_number)
        return phone_number

