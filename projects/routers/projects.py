from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.dependencies import get_db
from projects.crud import create_project, get_projects, get_project_by_id, update_project, delete_project
from auth.jwt import get_current_user
from core.models import User

router = APIRouter()

@router.post("/")
def create_project_route(name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Создание нового проекта для текущего пользователя.
    """
    return create_project(db=db, name=name, user_id=current_user.id)

@router.get("/")
def list_projects_route(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Получение списка проектов текущего пользователя.
    """
    return get_projects(db=db, user_id=current_user.id)

@router.get("/{project_id}")
def get_project_route(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Получение данных конкретного проекта, принадлежащего текущему пользователю.
    """
    project = get_project_by_id(db=db, project_id=project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found or access denied")
    return project

@router.put("/{project_id}")
def update_project_route(project_id: int, name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Обновление данных проекта текущего пользователя.
    """
    project = get_project_by_id(db=db, project_id=project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found or access denied")
    updated_project = update_project(db=db, project_id=project_id, name=name)
    return updated_project

@router.delete("/{project_id}")
def delete_project_route(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Удаление проекта текущего пользователя.
    """
    project = get_project_by_id(db=db, project_id=project_id)
    if not project or project.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found or access denied")
    if not delete_project(db=db, project_id=project_id):
        raise HTTPException(status_code=500, detail="Failed to delete project")
    return {"detail": "Project deleted successfully"}
