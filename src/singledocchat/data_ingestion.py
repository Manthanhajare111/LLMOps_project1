import uuid
from pathlib import Path
import sys
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from expections.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader

class SingleDocIngestor:
    def __init__(self):
        try:
            self.log = CustomLogger().get_logger(__file__)
        except Exception as e:
            self.log.error("Failed to initialize SingleDocIngestor",error=str(e))    
            raise DocumentPortalException("Logger Initialization Failed", sys)
        
    def ingest_files(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to ingest files",error=str(e))
            raise DocumentPortalException("File Ingestion Failed", sys)
        
    def _create_retriever(self):
        try:
            pass
        except Exception as e:           
            self.log.error("Failed to create retriever",error=str(e))
            raise DocumentPortalException("Retriever Creation Failed", sys)