from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from jinja2 import Template
from core.dependencies import get_db
from core.models import Project
from auth.jwt import get_current_user
from auth.oauth import check_google_token
import os

router = APIRouter()

# Путь к шаблонам HTML
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../templates")

def render_template(template_name: str, context: dict = {}):
    """
    Рендеринг HTML шаблона с использованием Jinja2.
    """
    with open(os.path.join(TEMPLATE_DIR, template_name), "r", encoding="utf-8") as file:
        template = Template(file.read())
    return template.render(context)

@router.get("/", response_class=HTMLResponse)
async def miniapps_home(request: Request, user=Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Главная страница Mini Apps. Проверка токенов и вывод списка проектов.
    """
    check_google_token(user)
    projects = db.query(Project).filter(Project.user_id == user.id).all()
    return render_template("index.html", {"request": request, "projects": projects})
