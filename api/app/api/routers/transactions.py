import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.core.security import get_current_user
from app.schemas.transactions import Transaction, TransactionCreate
from app.schemas.response import APIResponse, _success_response, _error_response, _not_found_response
from app.models.transaction import Transaction as TransactionModel

_logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/", response_model=APIResponse)
def read_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    _logger.info(f"User {current_user['username']} (ID: {current_user['id']}) fetching transactions")
    # Admin/developer can see all transactions, regular users only their own
    if current_user['role'] in ['admin', 'developer']:
        transactions = db.query(TransactionModel).offset(skip).limit(limit).all()
        _logger.info(f"Admin/Developer {current_user['username']} fetched {len(transactions)} transactions (all users)")
        return _success_response(f"Fetched {len(transactions)} transactions (all users)", transactions)
    else:
        transactions = db.query(TransactionModel).filter(TransactionModel.user_id == current_user['id']).offset(skip).limit(limit).all()
        _logger.info(f"User {current_user['username']} fetched {len(transactions)} transactions")
        return _success_response(f"Fetched {len(transactions)} transactions", transactions)


@router.post("/", response_model=APIResponse)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    _logger.info(f"User {current_user['username']} (ID: {current_user['id']}) creating new transaction")
    db_transaction = TransactionModel(**transaction.dict(), user_id=current_user['id'])
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    _logger.info(f"Transaction created successfully with ID: {db_transaction.id} by user {current_user['username']}")
    return _success_response("Transaction created successfully", db_transaction)


@router.get("/{transaction_id}", response_model=APIResponse)
def read_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    _logger.info(f"User {current_user['username']} (ID: {current_user['id']}) fetching transaction {transaction_id}")
    if current_user['role'] in ['admin', 'developer']:
        transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
        if transaction:
            _logger.info(f"Admin/Developer {current_user['username']} accessed transaction {transaction_id} (owned by user {transaction.user_id})")
    else:
        transaction = db.query(TransactionModel).filter(
            TransactionModel.id == transaction_id,
            TransactionModel.user_id == current_user['id']
        ).first()
        if transaction:
            _logger.info(f"User {current_user['username']} accessed their transaction {transaction_id}")

    if transaction is None:
        _logger.warning(f"Transaction {transaction_id} not found for user {current_user['username']}")
        raise HTTPException(status_code=404, detail="Transaction not found")
    return _success_response("Transaction retrieved successfully", transaction)


@router.put("/{transaction_id}", response_model=APIResponse)
def update_transaction(
    transaction_id: int,
    transaction_update: TransactionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    _logger.info(f"User {current_user['username']} (ID: {current_user['id']}) updating transaction {transaction_id}")
    if current_user['role'] in ['admin', 'developer']:
        transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
        if transaction:
            _logger.info(f"Admin/Developer {current_user['username']} updating transaction {transaction_id} (owned by user {transaction.user_id})")
    else:
        transaction = db.query(TransactionModel).filter(
            TransactionModel.id == transaction_id,
            TransactionModel.user_id == current_user['id']
        ).first()

    if transaction is None:
        _logger.warning(f"Transaction {transaction_id} not found for user {current_user['username']}")
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in transaction_update.dict().items():
        setattr(transaction, key, value)
    db.commit()
    db.refresh(transaction)
    _logger.info(f"Transaction {transaction_id} updated successfully by user {current_user['username']}")
    return _success_response("Transaction updated successfully", transaction)


@router.delete("/{transaction_id}", response_model=APIResponse)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    _logger.info(f"User {current_user['username']} (ID: {current_user['id']}) deleting transaction {transaction_id}")
    if current_user['role'] in ['admin', 'developer']:
        transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
        if transaction:
            _logger.info(f"Admin/Developer {current_user['username']} deleting transaction {transaction_id} (owned by user {transaction.user_id})")
    else:
        transaction = db.query(TransactionModel).filter(
            TransactionModel.id == transaction_id,
            TransactionModel.user_id == current_user['id']
        ).first()

    if transaction is None:
        _logger.warning(f"Transaction {transaction_id} not found for user {current_user['username']}")
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()
    _logger.info(f"Transaction {transaction_id} deleted successfully by user {current_user['username']}")
    return _success_response("Transaction deleted successfully")
