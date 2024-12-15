from sqlalchemy.orm import Session
from core.models import Project, AdAccount, OperationPeriod, Budget

# CRUD для проектов
def create_project(db: Session, name: str, user_id: int):
    project = Project(name=name, user_id=user_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_projects(db: Session, user_id: int):
    return db.query(Project).filter(Project.user_id == user_id).all()

def get_project_by_id(db: Session, project_id: int, user_id: int):
    # Проверка принадлежности проекта пользователю
    return db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()

def update_project(db: Session, user_id: int, project_id: int, name: str):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
    if project:
        project.name = name
        db.commit()
        db.refresh(project)
        return project
    return None

def delete_project(db: Session, user_id: int, project_id: int):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
    if project:
        db.delete(project)
        db.commit()
        return True
    return False

# CRUD для рекламных кабинетов
def create_ad_account(db: Session, user_id: int, project_id: int, platform: str, account_id: str, account_name: str):
    # Проверяем принадлежность проекта
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
    if not project:
        raise ValueError("Project does not belong to the current user.")
    ad_account = AdAccount(
        project_id=project_id,
        platform=platform,
        account_id=account_id,
        account_name=account_name
    )
    db.add(ad_account)
    db.commit()
    db.refresh(ad_account)
    return ad_account

def get_ad_accounts(db: Session, user_id: int, project_id: int):
    # Проверяем принадлежность проекта
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
    if not project:
        raise ValueError("Project does not belong to the current user.")
    return db.query(AdAccount).filter(AdAccount.project_id == project_id).all()

def delete_ad_account(db: Session, user_id: int, ad_account_id: int):
    ad_account = db.query(AdAccount).join(Project).filter(
        AdAccount.id == ad_account_id,
        Project.user_id == user_id
    ).first()
    if ad_account:
        db.delete(ad_account)
        db.commit()
        return True
    return False

# CRUD для операционных периодов
def create_operation_period(db: Session, user_id: int, project_id: int, name: str, start_date: str, end_date: str = None):
    # Проверяем принадлежность проекта
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
    if not project:
        raise ValueError("Project does not belong to the current user.")
    operation_period = OperationPeriod(
        project_id=project_id,
        name=name,
        start_date=start_date,
        end_date=end_date
    )
    db.add(operation_period)
    db.commit()
    db.refresh(operation_period)
    return operation_period

def get_operation_periods(db: Session, user_id: int, project_id: int):
    # Проверяем принадлежность проекта
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
    if not project:
        raise ValueError("Project does not belong to the current user.")
    return db.query(OperationPeriod).filter(OperationPeriod.project_id == project_id).all()

# CRUD для бюджетов
def create_budget(db: Session, user_id: int, project_id: int, operation_period_id: int, amount: float, ad_account_id: int = None, campaign_id: str = None):
    # Проверяем принадлежность проекта
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
    if not project:
        raise ValueError("Project does not belong to the current user.")
    budget = Budget(
        project_id=project_id,
        operation_period_id=operation_period_id,
        amount=amount,
        ad_account_id=ad_account_id,
        campaign_id=campaign_id
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget

def get_budgets(db: Session, user_id: int, project_id: int):
    # Проверяем принадлежность проекта
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
    if not project:
        raise ValueError("Project does not belong to the current user.")
    return db.query(Budget).filter(Budget.project_id == project_id).all()