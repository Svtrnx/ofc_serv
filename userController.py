from connection import get_user_by_username
from sqlalchemy.orm import Session

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db=db, username=username, password=password)
    if not user:
        return False
    return user