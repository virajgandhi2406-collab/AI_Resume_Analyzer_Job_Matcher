import re
import os
from typing import Dict, Any, Tuple, Optional
from pathlib import Path

class ResumeParser:
    """
    Parses PDF, DOCX, and TXT files and extracts raw text, candidate contact info,
    and structured sections (Experience, Education, Skills, Projects, Summary).
    """

    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extract plain text from PDF, DOCX, or TXT file"""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == ".pdf":
            return ResumeParser._extract_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            return ResumeParser._extract_docx(file_path)
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    @staticmethod
    def _extract_pdf(file_path: str) -> str:
        text = ""
        # Try pdfplumber first
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text
        except Exception:
            pass

        # Fallback to pypdf
        try:
            import pypdf
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            if text.strip():
                return text
        except Exception as e:
            pass

        return text.strip()

    @staticmethod
    def _extract_docx(file_path: str) -> str:
        try:
            import docx
            doc = docx.Document(file_path)
            text_runs = [para.text for para in doc.paragraphs if para.text.strip()]
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if cell.text.strip():
                            text_runs.append(cell.text.strip())
            return "\n".join(text_runs)
        except Exception as e:
            return ""

    @staticmethod
    def extract_contact_info(text: str) -> Dict[str, Optional[str]]:
        """Extract Name, Email, Phone, LinkedIn, GitHub, Location via Regex"""
        contact = {
            "name": None,
            "email": None,
            "phone": None,
            "linkedin": None,
            "github": None,
            "location": None
        }
        
        # Email
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact["email"] = email_match.group(0).strip()
            
        # Phone
        phone_pattern = r'(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?|\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact["phone"] = phone_match.group(0).strip()
            
        # LinkedIn
        linkedin_pattern = r'(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/([a-zA-Z0-9_-]+)'
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            contact["linkedin"] = f"https://linkedin.com/in/{linkedin_match.group(1)}"
            
        # GitHub
        github_pattern = r'(?:https?:\/\/)?(?:www\.)?github\.com\/([a-zA-Z0-9_-]+)'
        github_match = re.search(github_pattern, text, re.IGNORECASE)
        if github_match:
            contact["github"] = f"https://github.com/{github_match.group(1)}"
            
        # Name heuristic: Usually the first 1-3 non-empty lines
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for line in lines[:5]:
            if "@" not in line and "http" not in line and not any(char.isdigit() for char in line):
                words = line.split()
                if 1 <= len(words) <= 4:
                    contact["name"] = line
                    break

        return contact

    @staticmethod
    def extract_sections(text: str) -> Dict[str, str]:
        """Split resume into common sections using header markers"""
        sections = {
            "summary": "",
            "experience": "",
            "education": "",
            "skills": "",
            "projects": "",
            "certifications": ""
        }
        
        section_headers = {
            "summary": r'(summary|profile|about me|objective|professional summary)',
            "experience": r'(work experience|professional experience|employment history|experience|work history)',
            "education": r'(education|academic background|qualifications|academic history)',
            "skills": r'(technical skills|skills|technologies|core competencies|areas of expertise)',
            "projects": r'(projects|personal projects|key projects|academic projects)',
            "certifications": r'(certifications|certificates|licenses|courses|awards)'
        }
        
        # Build split pattern
        pattern = r'\n\s*(?:' + '|'.join([f'(?P<{k}>{v})' for k, v in section_headers.items()]) + r')\s*[:\n]'
        
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if not matches:
            # Fallback simple partition
            sections["summary"] = text[:500]
            sections["experience"] = text
            return sections

        for i in range(len(matches)):
            current_match = matches[i]
            section_name = None
            for key in section_headers.keys():
                if current_match.group(key):
                    section_name = key
                    break
            
            start_pos = current_match.end()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            
            if section_name:
                sections[section_name] = text[start_pos:end_pos].strip()

        return sections
