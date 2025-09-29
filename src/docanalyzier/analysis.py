import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from expections.custom_exception import DocumentPortalException
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
        self.logger.info("DocumentAnalyzer initialized with LLM and embedding model")

    def analyze(self, text: str, prompt_key: str) -> DocumentAnalysisResult:
        if prompt_key not in PROMPT_REGISTRY:
            error_msg = f"Prompt key '{prompt_key}' not found in registry"
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        prompt_template = PROMPT_REGISTRY[prompt_key]
        prompt = prompt_template.format(text=text)

        try:
            self.logger.info("Sending text to LLM for analysis", prompt_key=prompt_key)
            response = self.llm.predict(prompt)
            self.logger.info("LLM response received", response=response)

            parsed_result = self.output_parser.parse(response)
            self.logger.info("LLM response parsed successfully", parsed_result=parsed_result.dict())
            return parsed_result
        except Exception as e:
            self.logger.error("Error during document analysis", error=str(e))
            raise DocumentPortalException("Failed to analyze document", sys) from e