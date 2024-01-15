from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from model import Base, OfficeTableUser
from config import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASS
import datetime
from sqlalchemy.orm import Session
import schema

db_url = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(db_url)

Base.metadata.create_all(engine)


def get_current_user(current_user):
    Session = sessionmaker(bind=engine)
    session = Session()

    results = session.query(OfficeTableUser).filter(OfficeTableUser.username == current_user).all()

    session.close()

    return results

def get_user_only_by_username(db: Session, username: str):
    try:
        record = db.query(OfficeTableUser).filter((OfficeTableUser.username == username)).first()
        
        return record

    except Exception as e:
        db.rollback()
        return f"Error getting user by username: {e}"

def get_user_by_username(db: Session, username: str, password: str):
    try:
        record = db.query(OfficeTableUser).filter(
            (OfficeTableUser.username == username) & (OfficeTableUser.password == password)
        ).first()
        
        print(record)

        return record

    except Exception as e:
        db.rollback()
        return f"Error getting user by username: {e}"


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

session.close()
