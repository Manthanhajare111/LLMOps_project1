import sys
from dotenv import load_dotenv
import pandas as pd
from logger.custom_logger import CustomLogger
from expections.custom_exception import DocumentPortalException
from model.models import *
from prompt.prompt_lib import PROMPT_REGISTRY # type: ignore
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentComparer:
    def __init__(self):
        self.model_loader = ModelLoader()
        self.llm = self.model_loader.load_llm()
        self.logger = CustomLogger().get_logger(__file__)
        self.json_parser = JsonOutputParser(pydantic_object=SummaryResponse)
        self.output_parser = OutputFixingParser.from_llm(
            llm=self.llm,
            parser=self.json_parser
        )
        self.prompt = PROMPT_REGISTRY["document_comparison"]
        self.chain = self.prompt | self.llm | self.json_parser 
        self.log.info("DocumentComparer initialized with LLM and output parser")

    def compare_documents(self,combined_docs:str)-> pd.DataFrame:
        """Compares two documents and identifies differences.  """
        try:
            inputs= {
                "combined_docs": combined_docs,
                "format_instructions": self.output_parser.get_format_instructions()
            }
            self.log.info("Starting document comparison",inputs=inputs)
            response = self.chain.invoke(inputs)
            self.log.info("Document comparison completed", response=response)
            self._format_resposnse(response)

        except Exception as e:
            self.logg.error("Error during document comparison", error=str(e))
            raise DocumentPortalException("Failed to compare documents", sys) from e

    def _format_resposnse(self,response_parsed: list[dict])->pd.DataFrame:
        """Formats the comparison response."""
        try:
            df = pd.DataFrame(response_parsed)
            self.log.info("Formatted response into DataFrame", dataframe=df)
            return df
        except Exception as e:
            self.logg.error("Error during document comparison", error=str(e))
            raise DocumentPortalException("Failed to compare documents", sys) from e
