from pydantic import BaseModel
from typing import List, Optional


class TransactionSuggestion(BaseModel):
    category_id: int
    category_name: str
    confidence: float


class AISuggestionRequest(BaseModel):
    description: str
    amount: float
    type: str


class AISuggestionResponse(BaseModel):
    suggestions: List[TransactionSuggestion]


class BankStatementUpload(BaseModel):
    file: bytes
    filename: str


class ParsedTransaction(BaseModel):
    date: str
    description: str
    amount: float
    type: str
    category_suggestion: Optional[str] = None


class BankStatementResponse(BaseModel):
    transactions: List[ParsedTransaction]
    total_parsed: int
