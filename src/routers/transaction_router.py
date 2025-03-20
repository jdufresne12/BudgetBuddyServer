from typing import List
from fastapi import APIRouter, HTTPException, Depends # type: ignore
from ..services.transactions.transactions_service import TransactionService
from ..schemas.transactions import Transaction, CreateTransactionData, DeleteTransactionData, GetAllTransactionsData, GetMonthsTransactionsData
from ..utils.auth_token import verify_token

router = APIRouter(prefix='/transaction', tags=['transaction'])
transaction_service = TransactionService()

@router.post('/create_transaction', response_model=Transaction)
async def create_transaction(data: CreateTransactionData, token: dict = Depends(verify_token)):
    try:
        transaction = await transaction_service.create_transaction(data)
        if transaction:
            return transaction
        raise HTTPException(status_code=400, detail="Failed to create transaction")
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})
    
@router.post('/update_transaction', response_model=Transaction)
async def update_transaction(data: Transaction, token: dict = Depends(verify_token)):
    try:
        transaction = await transaction_service.update_transaction(data)
        if transaction:
            return transaction
        raise HTTPException(status_code=400, detail="Failed to update transaction")
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})
    
@router.delete('/delete_transaction', response_model=bool)
async def delete_transaction(data: DeleteTransactionData, token: dict = Depends(verify_token)):
    try:
        response = await transaction_service.delete_transaction(data)
        if response is True:
            return response 
        raise HTTPException(status_code=400, detail="Failed to delete transaction")
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})
    
@router.post('/get_all_transactions', response_model=List[Transaction])
async def get_all_transactions(data: GetAllTransactionsData, token: dict = Depends(verify_token)):
    try:
        transactions = await transaction_service.get_all_transactions(data)
        if transactions:
            return transactions
        raise HTTPException(status_code=400, detail="Failed to get all transactions")
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})
    
@router.post('/get_months_transactions', response_model=List[Transaction])
async def get_months_transactions(data: GetMonthsTransactionsData, token: dict = Depends(verify_token)):
    try:
        transactions = await transaction_service.get_months_transactions(data)
        if transactions:
            return transactions
        raise HTTPException(status_code=400, detail="Failed to get months transactions")
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})