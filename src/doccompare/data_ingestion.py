import sys
from pathlib import Path
import fitz
from logger.custom_logger import CustomLogger
from expections.custom_exception import DocumentPortalException

class DocumentComparer:

    def __init__(self,base_dir):
        self.logger = CustomLogger().get_logger(__file__)
        self.base_dir = Path(base_dir)
        self.base_dir.mk_dir(parents=True) = True, exist_ok=True

    def delete_existing_files(self,):
        try:
            if self.base_dir.exists() and self.base_dir.is_dir():
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                self.log.info("All files deleted successfully")
        except Exception as e:
            self.log.error("Error reading PDF file", error=str(e))
            raise DocumentPortalException("Failed to read PDF file", sys)

    def save_uploaded_file(self,reference_file,actual_file):
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

    def read_pdf(self,file_path)->str:
        """Reads the PDF and extracts text."""
        try:
            with fitz.open(self.file_path) as doc:
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