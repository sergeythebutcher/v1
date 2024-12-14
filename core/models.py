from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Enum,
    DECIMAL,
    Date,
    ForeignKey,
    TIMESTAMP,
    func
)
from sqlalchemy.orm import relationship
from core.db import Base

# Модель для пользователей
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), nullable=True)
    google_token = Column(String(255), nullable=True)
    google_refresh_token = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Связь с проектами
    projects = relationship("Project", back_populates="user")


# Модель для проектов
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Связи
    user = relationship("User", back_populates="projects")
    ad_accounts = relationship("AdAccount", back_populates="project")
    operation_periods = relationship("OperationPeriod", back_populates="project")
    budgets = relationship("Budget", back_populates="project")


# Модель для рекламных кабинетов
class AdAccount(Base):
    __tablename__ = "ad_accounts"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    platform = Column(Enum("google", "facebook"), nullable=False)
    account_id = Column(String(255), nullable=False)
    account_name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Связи
    project = relationship("Project", back_populates="ad_accounts")
    budgets = relationship("Budget", back_populates="ad_account")


# Модель для операционных периодов
class OperationPeriod(Base):
    __tablename__ = "operation_periods"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(Enum("weekly", "monthly", "custom_2_weeks", "custom_month", "custom_weeks"), nullable=False)
    start_date = Column(Date, nullable=True)  # Только для кастомных периодов
    end_date = Column(Date, nullable=True)    # Только для кастомных периодов
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Связи
    project = relationship("Project", back_populates="operation_periods")
    budgets = relationship("Budget", back_populates="operation_period")


# Модель для бюджетов
class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    operation_period_id = Column(Integer, ForeignKey("operation_periods.id", ondelete="CASCADE"), nullable=False)
    ad_account_id = Column(Integer, ForeignKey("ad_accounts.id", ondelete="CASCADE"), nullable=True)
    campaign_id = Column(String(255), nullable=True)  # NULL для бюджета уровня кабинета или проекта
    amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Связи
    project = relationship("Project", back_populates="budgets")
    ad_account = relationship("AdAccount", back_populates="budgets")
    operation_period = relationship("OperationPeriod", back_populates="budgets")
