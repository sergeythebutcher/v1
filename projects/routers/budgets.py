from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.dependencies import get_db
from projects.crud import create_budget, get_budgets

router = APIRouter()

@router.post("/")
def create_budget_route(project_id: int, operation_period_id: int, amount: float, ad_account_id: int = None, campaign_id: str = None, db: Session = Depends(get_db)):
    return create_budget(db=db, project_id=project_id, operation_period_id=operation_period_id, amount=amount, ad_account_id=ad_account_id, campaign_id=campaign_id)

@router.get("/")
def list_budgets_route(project_id: int, db: Session = Depends(get_db)):
    return get_budgets(db=db, project_id=project_id)
