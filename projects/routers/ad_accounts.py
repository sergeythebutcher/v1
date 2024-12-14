from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.dependencies import get_db
from projects.crud import create_ad_account, get_ad_accounts, delete_ad_account

router = APIRouter()

@router.post("/")
def create_ad_account_route(project_id: int, platform: str, account_id: str, account_name: str, db: Session = Depends(get_db)):
    return create_ad_account(db=db, project_id=project_id, platform=platform, account_id=account_id, account_name=account_name)

@router.get("/")
def list_ad_accounts_route(project_id: int, db: Session = Depends(get_db)):
    return get_ad_accounts(db=db, project_id=project_id)

@router.delete("/{ad_account_id}")
def delete_ad_account_route(ad_account_id: int, db: Session = Depends(get_db)):
    if not delete_ad_account(db=db, ad_account_id=ad_account_id):
        raise HTTPException(status_code=404, detail="Ad account not found")
    return {"detail": "Ad account deleted successfully"}
