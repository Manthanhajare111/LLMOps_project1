import uuid
from pathlib import Path
import sys
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from logger.custom_logger import CustomLogger
from excepctions.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader
from datetime import datetime, timezone

class SingleDocIngestor:
    def __init__(self,base_dir="src/data/singledocchat",faiss_dir: str = "faiss_index"): 
        try:
            self.log = CustomLogger().get_logger(__file__)
            self.data_dir = Path(base_dir)
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self.faiss_dir = Path(faiss_dir)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)
            self.model_loader = ModelLoader()
            self.log.info("SingleDocIngestor initialized", data_dir=str(self.data_dir),faiss_dir=str(self.faiss_dir))

        except Exception as e:
            self.log.error("Failed to initialize SingleDocIngestor",error=str(e))    
            raise DocumentPortalException("Logger Initialization Failed", sys)
        
    def ingest_files(self,uploaded_file):
        try:
            documents = []

            for uploaded_file in uploaded_file:
                unique_filename = f"session_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}[:8].pdf"
                temp_path = self.data_dir / unique_filename
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.read())
                self.log.info(f"File saved successfully at {temp_path}")
                loader = PyMuPDFLoader(str(temp_path))
                docs = loader.load()
                documents.extend(docs)
            self.log.info(f"Total {len(documents)} documents loaded successfully")

            return self._create_retriever(documents)
        except Exception as e:
            self.log.error("Failed to ingest files",error=str(e))
            raise DocumentPortalException("File Ingestion Failed", sys)
        
    def _create_retriever(self,documents):
        try:
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
            chunks = splitter.split_documents(documents)
            self.log.info("Documents split into chunks", chunk_count=len(chunks))

            embeddings = self.model_loader.load_embeddings()
            vector_Store = FAISS.from_documents(chunks, embeddings)

            vector_Store.save_local(str(self.faiss_dir))
            self.log.info("FAISS index created and saved successfully", faiss_dir=str(self.faiss_dir))

            retriver = vector_Store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
            self.log.info("Retriever created successfully")

            return retriver

        except Exception as e:           
            self.log.error("Failed to create retriever",error=str(e))
            raise DocumentPortalException("Retriever Creation Failed", sys)