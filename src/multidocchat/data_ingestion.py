import uuid
from pathlib import Path
import sys
from datetime import datetime, timezone
from langchian_community.document_loaders import PyPDFLoader,Docx2txtLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from excepctions.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader

class DocumentIngestor:
    SUPPORTED_FILE_TYPES = {".pdf", ".docx", ".txt"}
    def __init__(self, temp_dir="src/data/multidocchat",faiss_dir: str = "faiss_index", session_id:str | None = None):
        try:
            self.log = CustomLogger().get_logger(__file__)
            self.data_dir = Path(temp_dir)
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self.faiss_dir = Path(faiss_dir)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)

            ## session id for chat history
            self.session_id = session_id if session_id else f"session_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
            self.session_temp_dir = self.data_dir / self.session_id
            self.session_faiss_dir = self.faiss_dir / self.session_id
            self.session_temp_dir.mkdir(parents=True, exist_ok=True)
            self.session_faiss_dir.mkdir(parents=True, exist_ok=True)

             ## model loader instance
            self.model_loader = ModelLoader()
            self.log.info("ConversationalRAG initialized", data_dir=str(self.data_dir),faiss_dir=str(self.faiss_dir))
            
        except Exception as e:
            self.log.error("Failed to initialize ConversationalRAG",error=str(e))    
            raise DocumentPortalException("Logger Initialization Failed", sys)


    def ingest_files(self):
        try:
            documents = []
            for uploaded_file in uploaded_file:
                file_extension = Path(uploaded_file.name).suffix.lower()
                if file_extension not in self.SUPPORTED_FILE_TYPES:
                    self.log.warning(f"Unsupported file type: {file_extension}. Skipping file: {uploaded_file.name}")
                    continue
                
                unique_filename = f"{self.session_id}_{uuid.uuid4().hex[:8]}{file_extension}"
                temp_path = self.session_temp_dir / unique_filename
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())
                self.log.info(f"File saved successfully at {temp_path}")

                if file_extension == ".pdf":
                    loader = PyPDFLoader(str(temp_path))
                elif file_extension == ".docx":
                    loader = Docx2txtLoader(str(temp_path))
                elif file_extension == ".txt":
                    loader = TextLoader(str(temp_path))
                else:
                    self.log.warning(f"No loader available for file type: {file_extension}. Skipping file: {uploaded_file.name}")
                    continue

                docs = loader.load()
                documents.extend(docs)

                if not documents:
                    self.log.warning("No documents were loaded. Please check the uploaded files.")
                    raise DocumentPortalException("No documents loaded", sys)
            self.log.info(f"Total {len(documents)} documents loaded successfully")

            return self._create_retriever(documents)
        
        
        except Exception as e:
            self.log.error("Failed to ingest files",error=str(e))
            raise DocumentPortalException("File Ingestion Failed", sys)

    def _create_retriever(self):
        pass