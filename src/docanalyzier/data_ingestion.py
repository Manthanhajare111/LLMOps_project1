from __future__ import annotations
import os
import sys
import json
import uuid
import hashlib
import shutil
from pathlib import Path
from typing import Iterable, List, Optional, Dict, Any
import fitz  # PyMuPDF
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from utils.model_loader import ModelLoader
from logger import GLOBAL_LOGGER as log
from exceptions.custom_exception import DocumentPortalException


class DocumentHandler:
    """Handle pdf saving and reading operation.
    Automatically logs all actions and support session-based file management."""

    def __init__(self):
        pass

    def save_pdf(self):
        pass
    def read_pdf(self):
        pass
    