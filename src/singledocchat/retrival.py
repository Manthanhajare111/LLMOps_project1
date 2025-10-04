import sys
import os
from operator import itemgetter
from typing import List, Optional, Dict, Any

from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS

from utils.model_loader import ModelLoader
from exceptions.custom_exception import DocumentPortalException
from logger import GLOBAL_LOGGER as log
# from prompt.prompt_library import PROMPT_REGISTRY
from model.models import PromptType

class ConvsationalRAG:
    def __init__(self,session_id:str, retriever):
        try:
            pass
        except Exception as e:
            log.error("Failed to initialize ConvsationalRAG",error=str(e))    
            raise DocumentPortalException("ConvsationalRAG Initialization Failed", sys)
        
    def _load_llm(self):
        try:
            pass
        except Exception as e:
            log.error("Failed to load LLM",error=str(e))
            raise DocumentPortalException("LLM Loading Failed", sys)
        
    def _get_session_history(self):
        try:
            pass
        except Exception as e:
            log.error("Failed to get session history",error=str(e))
            raise DocumentPortalException("Session History Retrieval Failed", sys)
        
    def load_retriever(self):
        try:
            pass
        except Exception as e:
            log.error("Failed to load retriever",error=str(e))
            raise DocumentPortalException("Retriever Loading Failed", sys)
        
    def invoke(self):
        try:
            pass
        except Exception as e:
            log.error("Failed to invoke ConvsationalRAG",error=str(e),session_id=self.session_id)
            raise DocumentPortalException("ConvsationalRAG Invocation Failed", sys)