from pydantic import BaseModel, Field, RootModel 
from typing import List, Optional, Any,Union
from enum import Enum
class Metadata(BaseModel):
    summary: Optional[str] = Field(None, description="A brief summary of the document.")
    Title: str
    Author: str
    Datecreated: str
    Lastmodified: str
    Publisher: str
    Language: str
    PageCount: Union[int, str] 
    SentimentTone: str

class ChangeFormats(BaseModel):
    page : str
    changes : str

class SummaryResponse(RootModel[list[ChangeFormats]]):
    pass

class PromptType(str,Enum):
    DOCUMENT_ANALYSIS = "document_analysis"
    DOCUMENT_cOMPARISON = "document_comparison"
    CONTEXUALIZE_QUESTION = "contextualize_question"
    CONTEXT_QA = "context_qa"
