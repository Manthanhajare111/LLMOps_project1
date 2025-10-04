import sys
from pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from expections.custom_exception import DocumentPortalException
from typing import Iterable, List, Optional, Dict, Any

class DocumentIngestion:

    def __init__(self,base_dir="src/data/doccomapare",session_id: Optional[str] = None):
        self.log = CustomLogger().get_logger(__file__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.session_id = session_id # or generate_session_id()
        self.session_path = self.base_dir / self.session_id
        self.session_path.mkdir(parents=True, exist_ok=True)
        # log.info("DocumentComparator initialized", session_path=str(self.session_path))
        # self.file_path = file_path

    def delete_existing_files(self):
        try:
            if self.base_dir.exists() and self.base_dir.is_dir():
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                self.log.info("All files deleted successfully")
        except Exception as e:
            self.log.error("Error reading PDF file", error=str(e))
            raise DocumentPortalException("Failed to read PDF file", sys)

    def save_uploaded_files(self,reference_file,actual_file):
        """Saves the uploaded file to a temporary location."""
        try:
            self.delete_existing_files()
            self.log.info("Existing files deleted successfully")

            reference_path = self.base_dir/reference_file.name
            actual_path = self.base_dir/actual_file.name
            

            if not reference_file.name.endswith(".pdf") or not actual_file.name.endswith(".pdf"):
                raise ValueError("Only PDF files are supported.")
            
            with open(reference_path, "wb") as f:
                f.write(reference_file.getbuffer())

            with open(actual_path, "wb") as f:
                f.write(actual_file.getbuffer())
            
            self.log.info(f"Files saved successfully at {reference_path} and {actual_path}")
            return reference_path, actual_path
        except Exception as e:
            self.log.error("Error reading PDF file", error=str(e))
            raise DocumentPortalException("Failed to read PDF file", sys)

    def read_pdf(self,file_path:Path)->str:
        """Reads the PDF and extracts text."""
        try:
            # import pdb
            # pdb.set_trace()
            with fitz.open(file_path) as doc:
                if doc.is_encrypted:
                    raise ValueError("PDF is encrypted and cannot be read.")
                all_text = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    if text.strip():  # Check if the page has any text
                        all_text.append(f"\n --- Page {page_num + 1} ---\n{text}")
                self.log.info(f"Pdf read successfully {file_path} .Extracted text from {len(all_text)} pages.")
                return "\n".join(all_text)
        except Exception as e:
            self.log.error("Error reading PDF file", error=str(e))
            raise DocumentPortalException("Failed to read PDF file", sys) 
        
    def combine_documents(self)->str:
        try:
            content_dict = {}
            doc_parts = []

            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix == ".pdf":
                    content_dict[filename.name] = self.read_pdf(filename)

            for filename,content in content_dict.items():
                doc_parts.append(f"Document: {filename}\n{content}")

            combined_text = "\n\n".join(doc_parts)
            self.log.info("Documents combined successfully",count=len(doc_parts))
            return combined_text
        except Exception as e:
            self.log.error("Error combining documents", error=str(e))
            raise DocumentPortalException("Failed to combine documents", sys) 
        
    def clean_old_session(self,keep_latest=3):
        """ 
        Optional method to delete older session files, keeping only the latest 'keep_latest' files.
        """
        try:
            session_folders = sorted(
                [f for f in self.base_dir.iterdir() if f.is_dir()],
                reverse=True

            )
            for folder in session_folders[keep_latest:]:
                for file in folder.iterdir():
                    if file.is_file():
                        file.unlink()
                folder.rmdir()
                self.log.info(f"Deleted old session folder: {folder}")
        except Exception as e:
            self.log.error("Error cleaning old sessions", error=str(e))
            raise DocumentPortalException("Failed to clean old sessions", sys)