import uuid
from pathlib import Path
import sys
from datetime import datetime, timezone
from langchian_community.document_loaders import PyMuPDFLoader,Docx2txtLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logger import CustomLogger
from excepctions.custom_exception import DocumentPortalException
from utils.model_loader import ModelLoader

class ConversationalRAG:
   
    def load_retriever_from_faisse(self):
        pass

    def invoke(self):
        pass

    def _load_llm(self):
        try:
            llm = ModelLoader.load_llm()
            self.log.info("LLM loaded successfully",class_name= llm.__class__.__name__)
            return llm
        except Exception as e:
            log.error("Failed to load LLM",error=str(e))
            raise DocumentPortalException("LLM Loading Failed", sys)
        
    @staticmethod
    def _format_docs(docs):
        try:
            formatted_docs = "\n\n".join([doc.page_content for doc in docs])
            return formatted_docs
        except Exception as e:
            log.error("Failed to format documents",error=str(e))
            raise DocumentPortalException("Document Formatting Failed", sys)
        
    def _build_lcel_chain(self):
        try:
            prompt = PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]
            llm_chain = LLMChain(llm=self.llm, prompt=prompt)
            self.log.info("LLM Chain built successfully")
            return llm_chain
        except Exception as e:
            log.error("Failed to build LLM chain",error=str(e))
            raise DocumentPortalException("LLM Chain Building Failed", sys)