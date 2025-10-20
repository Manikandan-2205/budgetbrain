from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.ml_service import get_ai_suggestions, parse_bank_statement
from app.schemas.ml import AISuggestionRequest, AISuggestionResponse, BankStatementResponse
from app.models.user import User


router = APIRouter()


@router.post("/suggestions", response_model=AISuggestionResponse)
def get_transaction_suggestions(
    request: AISuggestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    suggestions = get_ai_suggestions(request, db)
    return AISuggestionResponse(suggestions=suggestions)


@router.post("/upload-statement", response_model=BankStatementResponse)
def upload_bank_statement(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.lower().endswith(('.pdf', '.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        contents = file.file.read()
        transactions = parse_bank_statement(contents, file.filename)
        return BankStatementResponse(
            transactions=transactions,
            total_parsed=len(transactions)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
