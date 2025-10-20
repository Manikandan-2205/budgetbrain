import openai
from typing import List
from app.core.config import settings
from app.schemas.ml import TransactionSuggestion, AISuggestionRequest, ParsedTransaction
from app.db.models import Category
from sqlalchemy.orm import Session


openai.api_key = settings.openai_api_key


def get_ai_suggestions(request: AISuggestionRequest, db: Session) -> List[TransactionSuggestion]:
    """
    Get AI-powered category suggestions for a transaction
    """
    categories = db.query(Category).all()
    category_list = "\n".join([f"- {cat.name} ({cat.type})" for cat in categories])

    prompt = f"""
    Based on the transaction description and amount, suggest the most appropriate category.
    Transaction: {request.description}
    Amount: {request.amount}
    Type: {request.type}

    Available categories:
    {category_list}

    Return the top 3 most likely categories with confidence scores (0-1).
    Format: Category Name: confidence_score
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.3
        )

        suggestions = []
        lines = response.choices[0].message.content.strip().split('\n')
        for line in lines[:3]:
            if ':' in line:
                cat_name, confidence = line.split(':', 1)
                cat_name = cat_name.strip()
                try:
                    confidence = float(confidence.strip())
                    category = next((c for c in categories if c.name.lower() == cat_name.lower()), None)
                    if category:
                        suggestions.append(TransactionSuggestion(
                            category_id=category.id,
                            category_name=category.name,
                            confidence=confidence
                        ))
                except ValueError:
                    continue

        return suggestions
    except Exception as e:
        print(f"AI suggestion error: {e}")
        return []


def parse_bank_statement(file_content: bytes, filename: str) -> List[ParsedTransaction]:
    """
    Parse bank statement and extract transactions
    This is a simplified implementation - in production, you'd use specialized libraries
    """
    # For demo purposes, return mock data
    # In real implementation, use libraries like tabula-py for PDFs or openpyxl for Excel
    mock_transactions = [
        ParsedTransaction(
            date="2023-10-01",
            description="Grocery Store Purchase",
            amount=-45.67,
            type="expense",
            category_suggestion="Food & Dining"
        ),
        ParsedTransaction(
            date="2023-10-02",
            description="Salary Deposit",
            amount=2500.00,
            type="income",
            category_suggestion="Salary"
        ),
        ParsedTransaction(
            date="2023-10-03",
            description="Gas Station",
            amount=-35.20,
            type="expense",
            category_suggestion="Transportation"
        )
    ]

    return mock_transactions
