import os
from pydantic import BaseModel
import pypdf
from docx import Document

class ParsedResume(BaseModel):
    text: str
    filename: str
    file_type: str

class ResumeParser:
    @staticmethod
    async def parse_file(file_path: str, filename: str) -> ParsedResume:
        ext = os.path.splitext(filename)[1].lower()
        text = ""
        
        if ext == ".pdf":
            text = ResumeParser._parse_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            text = ResumeParser._parse_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
            
        return ParsedResume(text=text, filename=filename, file_type=ext)

    @staticmethod
    def _parse_pdf(file_path: str) -> str:
        text = ""
        try:
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            raise
        return text

    @staticmethod
    def _parse_docx(file_path: str) -> str:
        text = ""
        try:
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            raise
        return text
