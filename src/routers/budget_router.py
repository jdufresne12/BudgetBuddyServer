from typing import List
from fastapi import APIRouter, HTTPException, Depends
from ..services.budget.budget_service import BudgetService
from ..schemas.budget import BudgetCategory, BudgetItem, BudgetItems, CreateBudgetItem, DeleteItemData, GetAllCategoriesData, GetBudgetData
from ..utils.auth_token import verify_token

router = APIRouter(prefix='/budget', tags=['budget'])
budget_service = BudgetService()

@router.post('/create_budget_item', response_model=BudgetItem)
async def create_budget_item(data: CreateBudgetItem, token: dict = Depends(verify_token)):
    try:
        budget_item = await budget_service.create_budget_item(data)
        if budget_item:
            return BudgetItem(
                item_id = budget_item.item_id,
                section = budget_item.section,
                user_id = budget_item.user_id,
                name = budget_item.name,
                amount = budget_item.amount,
                type = budget_item.type,
                start_date = budget_item.start_date,
                end_date = budget_item.end_date
            )
        raise HTTPException(status_code=400, detail="Failed to create budget item")
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})

@router.delete('/delete_budget_item', response_model=bool)
async def delete_budget_item(data: DeleteItemData, token: dict = Depends(verify_token)):
    try:
        deleted = await budget_service.delete_budget_item(data)
        if deleted is True:
            return True
        raise HTTPException(status_code=400, detail="Item not found or doesn't belong to user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post('/update_budget_item', response_model=BudgetItem)
async def update_budget_item(data: BudgetItem, token: dict = Depends(verify_token)):
    try:
        budget_item = await budget_service.update_budget_item(data)
        if budget_item:
            return BudgetItem(
                item_id = budget_item.item_id,
                section = budget_item.section,
                user_id = budget_item.user_id,
                name = budget_item.name,
                amount = budget_item.amount,
                type = budget_item.type,
                start_date = budget_item.start_date,
                end_date = budget_item.end_date
            )
        raise HTTPException(status_code=400, detail="Failed to update budget item")
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})
    
@router.post('/get_budget', response_model=List[BudgetItems])
async def get_budget(data: GetBudgetData, token: dict = Depends(verify_token)):
    try:
        budget = await budget_service.get_budget(data)
        return budget
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/get_all_categories', response_model=List[BudgetCategory])
async def get_all_categories(data: GetAllCategoriesData, token: dict = Depends(verify_token)):
    try:
        categories = await budget_service.get_all_categories(data)
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
