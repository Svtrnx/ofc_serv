from sqlalchemy import create_engine, and_, desc, func, extract, Integer, case, literal
from sqlalchemy.orm import sessionmaker
from model import Base, OfficeTableUser, OfficeTablePc, OfficeTablePhoneNumber, OfficeTablePromocodes, OfficeTableLog
from config import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASS
import datetime
from sqlalchemy.orm import Session
import schema
from typing import List
from datetime import datetime, timedelta


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

def get_logs_query():
	Session = sessionmaker(bind=engine)
	session = Session()

	results = session.query(OfficeTableLog).all()

	session.close()

	return results

def get_user_only_by_username(db: Session, username: str):
	try:
		record = db.query(OfficeTableUser).filter((OfficeTableUser.username == username)).first()
		
		return record

	except Exception as e:
		db.rollback()
		return f"Error getting user by username: {e}"
	
def get_users_usernames(db: Session):
	try:
		users = db.query(OfficeTableUser).all()
		usernames = [user.username for user in users]
		print(usernames)
		return usernames
	except Exception as e:
		db.rollback()
		return f"Error getting users usernames: {e}"

def get_users(db: Session, current_user):
	try:
		users = db.query(OfficeTableUser).all()
		user_info = [(user.id, user.username, user.balance, user.status, user.language, user.reg_datetime) for user in users]

		# filtered_users = [user for user in user_info if user[1] != current_user]

		return user_info
	except Exception as e:
		db.rollback()
		return f"Error getting users: {e}"


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

	return {'phone_number': 'No numbers in database!'}

def get_phone_numbers_stats(db):
	today = datetime.now().date()

	stats_query = db.query(
		func.sum(case((OfficeTablePhoneNumber.missed == True, 1), else_=0)),
		func.sum(case((OfficeTablePhoneNumber.processed == True, 1), else_=0)),
		func.sum(case((OfficeTablePhoneNumber.recall == True, 1), else_=0)),
		func.sum(case((OfficeTablePhoneNumber.decline == True, 1), else_=0)),
		func.count(OfficeTablePhoneNumber.id)
	).filter(
		OfficeTablePhoneNumber.used == True,
		OfficeTablePhoneNumber.done_number_datetime >= (today - timedelta(days=12)),
		OfficeTablePhoneNumber.done_number_datetime < today
	).first()

	result = {
		"missed": stats_query[0] or 0,
		"processed": stats_query[1] or 0,
		"recall": stats_query[2] or 0,
		"decline": stats_query[3] or 0,
		"total": stats_query[4] or 0
	}

	return result



def get_daily_stats(db):
	today = datetime.now().date()
	twelve_days_ago = today - timedelta(days=14)

	daily_stats = db.query(
		func.date(OfficeTablePhoneNumber.done_number_datetime).label("date"),
		func.sum(case((OfficeTablePhoneNumber.missed == True, 1), else_=0)).label("missed"),
		func.sum(case((OfficeTablePhoneNumber.processed == True, 1), else_=0)).label("processed"),
		func.sum(case((OfficeTablePhoneNumber.recall == True, 1), else_=0)).label("recall"),
		func.sum(case((OfficeTablePhoneNumber.decline == True, 1), else_=0)).label("decline")
	).filter(
		OfficeTablePhoneNumber.used == True,
		func.date(OfficeTablePhoneNumber.done_number_datetime) >= twelve_days_ago,
		func.date(OfficeTablePhoneNumber.done_number_datetime) < today + timedelta(days=1)  # Adjusted to include today
	).group_by(func.date(OfficeTablePhoneNumber.done_number_datetime)).all()

	result = {}
	for stat in daily_stats:
		days_difference = (today - stat.date).days
		day_key = f"day{days_difference}"
		result[day_key] = {
			"missed": stat.missed or 0,
			"processed": stat.processed or 0,
			"recall": stat.recall or 0,
			"decline": stat.decline or 0
		}

	return result



def create_phone_numbers(db: Session, media: List[schema.OfficeNumberSchema]):
	new_numbers = [
		OfficeTablePhoneNumber(
			phone_number=number.phone_number,
			is_active=number.is_active,
			used=number.used,
			missed=number.missed,
			processed=number.processed,
			recall=number.recall,
			decline=number.decline,
			phone_datetime=number.phone_datetime,
		)
		for number in media
	]
	db.add_all(new_numbers)
	db.commit()

def create_log(db: Session, log: schema.OfficeLogSchema):
	new_log = OfficeTableLog(
		log_info       	= log.log_info,
		username        = log.username,
		log_datetime    = log.log_datetime,
	)
	db.add(new_log)
	db.commit()
	db.refresh(new_log)
	return new_log

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



def create_user(db: Session, user: schema.OfficeUserSchema):
	new_user = OfficeTableUser(
		username       	= user.username,
		password        = user.password,
		balance    		= user.balance,
		status    		= user.status,
		language    	= user.language,
		reg_datetime    = user.reg_datetime,
	)
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	return new_user



def delete_users(db: Session, user_send: List[List[str]]):
    try:
        print(user_send)
        for user_data in user_send:
            print(user_data)
            print(user_data[0])
            print(user_data[1])
            filter_criteria = and_(
                OfficeTableUser.username == user_data[0],
                OfficeTableUser.status == user_data[1]
            )

            user_to_delete = db.query(OfficeTableUser).filter(filter_criteria).first()

            if user_to_delete:
                db.delete(user_to_delete)

        db.commit()
        return {'status': 'successfully deleted'}

    except Exception as e:
        db.rollback()
        return f"Error deleting users: {e}"

 
 
def get_user_password(db: Session, username: str):
	try:
		user = db.query(OfficeTableUser).filter(
			(OfficeTableUser.username == username) & (OfficeTableUser.status == 'Moderator')
		).first()

		if user:
			return user.password
		else:
			return 'Dont find user'

	except Exception as e:
		db.rollback()
		return f"Error getting user password by username: {e}"
 
 
 
 
 
 
 
 
 
 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

session.close()
