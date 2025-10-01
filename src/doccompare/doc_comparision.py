import sys
from dotenv import load_env
import pandas
from logger.custom_logger import CustomLogger
from expections.custom_exception import DocumentPortalException
from model.models import *
from prompt.prompt_library import PROMPT_REGISTRY # type: ignore
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser

class DocumentComparer:
    def __init__(self):
        pass

    def compare_documents(self):
        """Compares two documents and identifies differences.  """
        pass

    def _format_resposnse(self):
        """Formats the comparison response."""
        pass
    