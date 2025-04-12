import os

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///database/moovies.db"

Base = declarative_base()

def get_engine():
    if not os.path.exists('database'):
        os.makedirs('database')
    return create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = get_engine())

class DatabaseConfig:
    
    def __init__(self):
        self.criar_tabelas()

    def criar_tabelas(self):
        engine = get_engine()
        Base.metadata.create_all(bind = engine)
        
    def get_db(self):
        db: Session = SessionLocal()
        
        try:
            yield db
        finally:
            db.close()        
                
    @contextmanager
    def session_scope(self):
        db: Session = SessionLocal()
        
        try:
            yield db
        finally:
            db.close()
