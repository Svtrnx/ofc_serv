from sqlalchemy import create_engine, and_, desc
from sqlalchemy.orm import sessionmaker
from model import Base, OfficeTableUser, OfficeTablePc, OfficeTablePhoneNumber, OfficeTablePromocodes
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

def get_promos(current_user):
    Session = sessionmaker(bind=engine)
    session = Session()

    results = session.query(OfficeTablePromocodes).filter(OfficeTablePromocodes.username == current_user).all()

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
    
def query_pc_chain(hwid, pc_name):
    Session = sessionmaker(bind=engine)
    session = Session()

    results = session.query(OfficeTablePc).filter((OfficeTablePc.hwid == hwid)
                            & (OfficeTablePc.pc_name == pc_name)).all()

    session.close()

    return results

def get_phone_number(db):
    number = db.query(OfficeTablePhoneNumber) \
        .filter(
            (OfficeTablePhoneNumber.is_active == False) &
            (OfficeTablePhoneNumber.used == False) &
            (OfficeTablePhoneNumber.missed == False) &
            (OfficeTablePhoneNumber.processed == False) &
            (OfficeTablePhoneNumber.recall == False) &
            (OfficeTablePhoneNumber.decline == False)
        ) \
        .order_by(OfficeTablePhoneNumber.phone_datetime) \
        .first()

    if number:
        number_data = {
            "id": 					number.id,
            "phone_number": 		number.phone_number,
            "phone_info": 			number.phone_info,
            "is_active": 			number.is_active,
            "used": 				number.used,
            "missed": 				number.missed,
            "processed": 			number.processed,
            "recall": 				number.recall,
            "decline": 				number.decline,
            "phone_datetime": 		number.phone_datetime,
            "recall_time": 			number.recall_time,
            "done_number_datetime": number.done_number_datetime,
        }

        db.query(OfficeTablePhoneNumber) \
            .filter(OfficeTablePhoneNumber.id == number.id) \
            .update({"is_active": True})
        
        db.commit()

        return number_data

    return None

def create_phone_number(db: Session, media: schema.OfficeNumberSchema):
    new_number = OfficeTablePhoneNumber(
        phone_number        = media.phone_number,
        is_active          	= media.is_active,
        used          		= media.used,
        missed        		= media.missed,
        processed        	= media.processed,
        recall        		= media.recall,
        decline        		= media.decline,
        phone_datetime      = media.phone_datetime,
    )
    print(new_number)
    db.add(new_number)
    db.commit()
    db.refresh(new_number)
    return new_number

def create_pc_chain(db: Session, media: schema.OfficePcSchema):
    new_pc = OfficeTablePc(
        hwid             = media.hwid,
        pc_name          = media.pc_name,
        activated        = media.activated,
    )
    print(new_pc)
    db.add(new_pc)
    db.commit()
    db.refresh(new_pc)
    return new_pc


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

session.close()
