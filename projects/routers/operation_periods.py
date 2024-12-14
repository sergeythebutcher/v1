from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.dependencies import get_db
from projects.crud import create_operation_period, get_operation_periods

router = APIRouter()

@router.post("/")
def create_operation_period_route(project_id: int, name: str, start_date: str, end_date: str = None, db: Session = Depends(get_db)):
    return create_operation_period(db=db, project_id=project_id, name=name, start_date=start_date, end_date=end_date)

@router.get("/")
def list_operation_periods_route(project_id: int, db: Session = Depends(get_db)):
    return get_operation_periods(db=db, project_id=project_id)
