from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Time, create_engine

DATABASE_NAME = 'app.db'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    status = Column(Boolean)
    deadline = Column(Time)
    priority = Column(Integer)
    category_id = Column(Integer, ForeignKey('category.id'))


def create_db():
    Base.metadata.create_all(engine)


create_db()
