from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.dependencies import get_db
from auth.jwt import get_current_user
from projects.crud import create_operation_period, get_operation_periods
from core.models import User, Project

router = APIRouter()

@router.post("/")
def create_operation_period_route(
    project_id: int,
    name: str,
    start_date: str,
    end_date: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Проверяем, принадлежит ли проект текущему пользователю
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=403, detail="You do not have access to this project.")
    
    return create_operation_period(db=db, project_id=project_id, name=name, start_date=start_date, end_date=end_date)

@router.get("/")
def list_operation_periods_route(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Проверяем, принадлежит ли проект текущему пользователю
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=403, detail="You do not have access to this project.")
    
    return get_operation_periods(db=db, project_id=project_id)
