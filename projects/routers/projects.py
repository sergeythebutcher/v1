from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.dependencies import get_db
from projects.crud import create_project, get_projects, get_project_by_id, update_project, delete_project

router = APIRouter()

@router.post("/")
def create_project_route(name: str, user_id: int, db: Session = Depends(get_db)):
    return create_project(db=db, name=name, user_id=user_id)

@router.get("/")
def list_projects_route(user_id: int, db: Session = Depends(get_db)):
    return get_projects(db=db, user_id=user_id)

@router.get("/{project_id}")
def get_project_route(project_id: int, db: Session = Depends(get_db)):
    project = get_project_by_id(db=db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}")
def update_project_route(project_id: int, name: str, db: Session = Depends(get_db)):
    project = update_project(db=db, project_id=project_id, name=name)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}")
def delete_project_route(project_id: int, db: Session = Depends(get_db)):
    if not delete_project(db=db, project_id=project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return {"detail": "Project deleted successfully"}
