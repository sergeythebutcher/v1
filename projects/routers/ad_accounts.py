from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.dependencies import get_db
from auth.jwt import get_current_user
from projects.crud import create_ad_account, get_ad_accounts, delete_ad_account
from core.models import User

router = APIRouter()

@router.post("/")
def create_ad_account_route(
    project_id: int, 
    platform: str, 
    account_id: str, 
    account_name: str, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Проверяем, что проект принадлежит текущему пользователю
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=403, detail="Access denied to this project")
    
    # Создаем рекламный аккаунт
    return create_ad_account(db=db, project_id=project_id, platform=platform, account_id=account_id, account_name=account_name)

@router.get("/")
def list_ad_accounts_route(
    project_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Проверяем, что проект принадлежит текущему пользователю
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=403, detail="Access denied to this project")
    
    # Получаем рекламные аккаунты
    return get_ad_accounts(db=db, project_id=project_id)

@router.delete("/{ad_account_id}")
def delete_ad_account_route(
    ad_account_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Проверяем, что рекламный аккаунт принадлежит проекту текущего пользователя
    ad_account = db.query(AdAccount).join(Project).filter(
        AdAccount.id == ad_account_id,
        Project.user_id == current_user.id
    ).first()
    if not ad_account:
        raise HTTPException(status_code=404, detail="Ad account not found or access denied")
    
    # Удаляем рекламный аккаунт
    if not delete_ad_account(db=db, ad_account_id=ad_account_id):
        raise HTTPException(status_code=404, detail="Ad account not found")
    return {"detail": "Ad account deleted successfully"}
