from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy

DATABASE_NAME = 'app.db'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)

db = SQLAlchemy()


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

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    sorting: str = Column(String)
    filtering: str = Column(String, default='skip')


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

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String)
    description: str = Column(String)
    status: bool = Column(Boolean)
    deadline: DateTime = Column(DateTime)
    priority: int = Column(Integer, default=6)
    category_id: int = Column(Integer, ForeignKey('category.id'))
