from typing import Any
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, sessionmaker
from sqlalchemy import Column, ForeignKey, create_engine, Integer, String, Boolean, DateTime
from flask_sqlalchemy import SQLAlchemy

DATABASE_NAME: str = 'app.db'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session: sessionmaker = sessionmaker(bind=engine)

db: Any = SQLAlchemy()


class Category(db.Model):
    """
    Класс, представляющий категорию.

    Attributes:
        id (int): Уникальный идентификатор категории.
        name (str): Название категории.
        sorting (str): Метод сортировки для категории.
        filtering (str): Метод фильтрации для категории.
    """
    __tablename__ = 'category'

    id: Column[int] = Column(Integer, primary_key=True)
    name: Column[str] = Column(String)
    sorting: Column[str] = Column(String)
    filtering: Column[str] = Column(String, default='skip')


class Tasks(db.Model):
    """
    Класс, представляющий задачу.

    Attributes:
        id (int): Уникальный идентификатор задачи.
        title (str): Заголовок задачи.
        description (str): Описание задачи.
        status (bool): Статус задачи (True, если выполнена, False в противном случае).
        deadline (DateTime): Срок выполнения задачи.
        priority (int): Приоритет задачи.
        category_id (int): ID категории, к которой принадлежит задача.
    """
    __tablename__ = 'tasks'

    id: Column[int] = Column(Integer, primary_key=True)
    title: Column[str] = Column(String)
    description: Mapped[str] = mapped_column(default='')
    status: Column[bool] = Column(Boolean)
    deadline: Mapped[datetime] = mapped_column(default=datetime.now())
    priority: Column[int] = Column(Integer, default=6)
    category_id: Column[int] = Column(Integer, ForeignKey('category.id'))
