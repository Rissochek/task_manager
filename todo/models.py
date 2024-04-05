from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Time, create_engine
from flask_sqlalchemy import SQLAlchemy

DATABASE_NAME = 'app.db'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)

db = SQLAlchemy()


class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Tasks(db.Model):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    status = Column(Boolean)
    deadline = Column(Time)
    priority = Column(Integer)
    category_id = Column(Integer, ForeignKey('category.id'))

