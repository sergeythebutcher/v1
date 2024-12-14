from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from core.db import SessionLocal
from core.models import User, Project, Budget

router = APIRouter()

@router.get("/miniapps/dashboard")
def miniapps_dashboard(telegram_id: str, db: Session = Depends(SessionLocal)):
    """
    Отображение данных пользователя в Mini App.
    """
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Получение проектов и данных по расходам
    projects = db.query(Project).filter(Project.user_id == user.id).all()
    budgets = db.query(Budget).filter(Budget.project_id.in_([p.id for p in projects])).all()

    return {
        "user": {"telegram_id": user.telegram_id, "email": user.email},
        "projects": [{"id": p.id, "name": p.name} for p in projects],
        "budgets": [{"id": b.id, "amount": b.amount} for b in budgets]
    }
