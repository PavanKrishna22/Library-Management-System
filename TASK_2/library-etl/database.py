from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

#engine
def get_engine(db_url: str):
    return create_engine(db_url)

#session
def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

def create_tables(engine):
    Base.metadata.create_all(engine)
