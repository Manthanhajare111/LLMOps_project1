import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from excepctions.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from prompt.prompt_library import PROMPT_REGISTRY # type: ignore

class DocumentAnalyzer:
    """
    Analyzes documents using LLMs and predefined prompts.
    """

    def __init__(self):
        self.model_loader = ModelLoader()
        self.llm = self.model_loader.load_llm()
        self.embedding_model = self.model_loader.load_embeddings()
        self.logger = CustomLogger().get_logger(__file__)
        self.json_parser = JsonOutputParser(pydantic_object=Metadata)
        self.output_parser = OutputFixingParser.from_llm(
            llm=self.llm,
            parser=self.json_parser
        )
        self.prompt = PROMPT_REGISTRY["document_analysis"]
        self.logger.info("DocumentAnalyzer initialized with LLM and embedding model")

    def analyze(self, text: str, prompt_key: str) -> dict:
        try:
            chain = self.prompt | self.llm | self.output_parser
            
            self.log.info("Metadata-analyziz chain initialized")
            response = chain.invoke({
                "format_instructions": self.output_parser.get_format_instructions(),
                "document_text": text
            })
            self.log.info("Metadata-Extraction successful",key=list(response.keys()))
            return response
        
        except Exception as e:
            self.logger.error("Error during document analysis", error=str(e))
            raise DocumentPortalException("Failed to analyze document", sys) from e