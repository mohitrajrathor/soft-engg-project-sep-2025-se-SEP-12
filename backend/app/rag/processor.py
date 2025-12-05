import os
import logging
from typing import List, Dict, Any
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
import pandas as pd
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.rag.ocr import DeepSeekOCR

logger = logging.getLogger(__name__)

class ContentProcessor:
    def __init__(self, ocr_enabled: bool = True):
        self.ocr_enabled = ocr_enabled
        if self.ocr_enabled:
            try:
                self.ocr = DeepSeekOCR()
            except Exception as e:
                logger.warning(f"Could not initialize DeepSeek OCR: {e}. OCR will be disabled.")
                self.ocr_enabled = False
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def process_file(self, file_path: str, file_type: str) -> List[str]:
        """Process a file and return a list of text chunks."""
        logger.info(f"Processing file: {file_path} ({file_type})")
        
        text_content = ""
        
        try:
            if file_type == '.pdf':
                text_content = self._process_pdf(file_path)
            elif file_type in ['.doc', '.docx']:
                text_content = self._process_docx(file_path)
            elif file_type in ['.xls', '.xlsx']:
                text_content = self._process_excel(file_path)
            elif file_type == '.txt':
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text_content = f.read()
            elif file_type == 'html' or file_type == '.html':
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    text_content = soup.get_text(separator='\n')
            else:
                logger.warning(f"Unsupported file type: {file_type}")
                return []

            if not text_content:
                logger.warning(f"No content extracted from {file_path}")
                return []

            # Split text into chunks
            chunks = self.text_splitter.split_text(text_content)
            return chunks

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return []

    def _process_pdf(self, file_path: str) -> str:
        """Extract text from PDF, using OCR if enabled."""
        text = ""
        doc = fitz.open(file_path)
        
        for page_num, page in enumerate(doc):
            # Try to extract text directly first
            page_text = page.get_text()
            
            if page_text.strip():
                text += page_text + "\n"
            elif self.ocr_enabled:
                # If no text found (scanned PDF), use OCR
                logger.info(f"No text found on page {page_num} of {file_path}. Using OCR.")
                pix = page.get_pixmap()
                img_path = f"{file_path}_page_{page_num}.png"
                pix.save(img_path)
                
                ocr_text = self.ocr.extract_text_from_image(img_path)
                text += ocr_text + "\n"
                
                # Cleanup temp image
                if os.path.exists(img_path):
                    os.remove(img_path)
                    
        return text

    def _process_docx(self, file_path: str) -> str:
        """Extract text from DOCX."""
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    def _process_excel(self, file_path: str) -> str:
        """Extract text from Excel."""
        # Read all sheets
        dfs = pd.read_excel(file_path, sheet_name=None)
        text = ""
        for sheet_name, df in dfs.items():
            text += f"Sheet: {sheet_name}\n"
            text += df.to_string() + "\n\n"
        return text
