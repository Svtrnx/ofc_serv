
from fastapi import Depends, APIRouter, Request, Body, Response, HTTPException, status, Form, Cookie
from sqlalchemy.orm import Session
from connection import session, get_db, get_current_user, create_pc_chain, query_pc_chain, get_phone_number, get_promos, create_phone_numbers, create_log, get_logs_query, get_users_usernames
from schema import Token
import model
import userController
from datetime import timedelta, datetime
from dotenv import load_dotenv
from starlette.responses import RedirectResponse
from authSecurity import get_current_user, create_access_token
from config import ACCESS_TOKEN_EXPIRE_MINUTES, COOKIE_NAME
from typing import List

load_dotenv()
userRouter = APIRouter()

@userRouter.get("/index")
def get_index(request: Request):
	return {"request": request.url}

@userRouter.post("/create-log")
async def create_log_func(log_info: str = Body(embed=True), db: Session = Depends(get_db), current_user: model.OfficeTableUserRequestForm = Depends(get_current_user)):
	try:
		current_time = datetime.now() + timedelta(hours=2)
		new_log = model.OfficeTableLog (
			log_info=log_info,
			username=current_user.username,
			log_datetime=current_time,
		)
		log = create_log(db=db, log=new_log)
		return log
	except Exception as e:
		raise HTTPException(status_code=511, detail=f"Error: {e}")

@userRouter.get('/get-logs')
async def get_logs(current_user: model.OfficeTableUserRequestForm = Depends(get_current_user)):
	if current_user.status == 'Moderator' or current_user.status == 'Admin':
		logs = get_logs_query()
		return logs
	else:
		raise HTTPException(status_code=401, detail=f"Access denied")

@userRouter.get('/get-usernames')
async def get_logs(db: Session = Depends(get_db), current_user: model.OfficeTableUserRequestForm = Depends(get_current_user)):
	if current_user.status == 'Moderator' or current_user.status == 'Admin':
		usernames = get_users_usernames(db=db)
		return usernames
	else:
		raise HTTPException(status_code=401, detail=f"Access denied")

@userRouter.post('/signin', response_model=Token)
async def signin_auth(response:Response, db: Session = Depends(get_db), form_data: model.OAuth2PasswordRequestFormSignin = Depends()):
	user = userController.authenticate_user(
		db=db,
		username=form_data.username,
		password=form_data.password
	)
	if not user:
		raise HTTPException(status_code=301, detail="Incorrect account information")
	
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={"sub": user.username}, expires_delta=access_token_expires
	)
	response = RedirectResponse(url='/index',status_code=status.HTTP_302_FOUND)
	response.set_cookie(key="access_token",value=f"Bearer {access_token}", samesite='none', httponly=True,
					secure=True, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 600) 
	return response


@userRouter.get('/get-user')
async def get_user(db: Session = Depends(get_db), current_user: model.OfficeTableUserRequestForm = Depends(get_current_user)):
	try:	
		user = current_user
		return user.json()
	except Exception as e:
			raise HTTPException(status_code=511, detail=f"Error: {e}")

@userRouter.get('/get-promos')
async def get_user(db: Session = Depends(get_db), current_user: model.OfficeTableUserRequestForm = Depends(get_current_user)):
	promos = get_promos(current_user.username)
	return {"promos": promos}

@userRouter.post('/chain-pc')
def get_user(db: Session = Depends(get_db), form_data: model.OfficeTablePcRequestForm = Depends()):
	try:
		pc_exists = query_pc_chain(hwid=form_data.hwid, pc_name=form_data.pc_name)
  
		if not pc_exists:
			current_time = datetime.now() + timedelta(hours=2)	
			new_pc = model.OfficeTablePc(
				hwid=form_data.hwid,
				pc_name=form_data.pc_name,
				activated=current_time
			)
			pc = create_pc_chain(db=db, media=new_pc)
			return {'pc': pc}
	except Exception as e:
		raise HTTPException(status_code=511, detail=f"Error: {e}")

@userRouter.post('/create-numbers')
def create_numbers(phone_numbers: List[str] = Body(...), db: Session = Depends(get_db), current_user: model.OfficeTableUserRequestForm = Depends(get_current_user)):
    if current_user.status == 'Moderator' or current_user.status == 'Admin':
        try:
            current_time = datetime.now() + timedelta(hours=2)
            new_numbers = [
                model.OfficeTablePhoneNumber(
                    phone_number=number,
                    is_active=False,
                    used=False,
                    missed=False,
                    processed=False,
                    recall=False,
                    decline=False,
                    phone_datetime=current_time,
                )
                for number in phone_numbers
            ]
            create_phone_numbers(db=db, media=new_numbers)
            return {'status': 'success'}
        except Exception as e:
            raise HTTPException(status_code=511, detail=f"Error: {e}")
    else:
        raise HTTPException(status_code=401, detail=f"Access denied")

@userRouter.get('/get-phone-number')
async def get_number(db: Session = Depends(get_db), current_user: model.OfficeTableUserRequestForm = Depends(get_current_user)):
	phone_number = get_phone_number(db=db)
	print(phone_number)
	return {'number': phone_number}
	

@userRouter.patch('/update-user-info')
async def create_task(
	username: str = Body(embed=True),
	password: str = Body(embed=True),
	language: str = Body(embed=True),
	db: Session = Depends(get_db),
	form_data: model.OfficeTableUserShortRequestForm = Depends(),
  	current_user: model.OfficeTableUserRequestForm = Depends(get_current_user)
):
	if current_user.username == username and current_user.password == password:
		form_data.username 	= username
		form_data.password 	= password
		form_data.language 	= language
		
		db_user = db.query(model.OfficeTableUser).filter_by(
			username=form_data.username,
			password=form_data.password,
		).first()
	
		
		if db_user:
			if form_data.language:
				db_user.language = form_data.language
	
			db.commit()
			db.refresh(db_user)
			return {"user": db_user}
		else:
			return {"error": "User dont found"}
	else:
		raise HTTPException(status_code=311, detail="Error user data")


@userRouter.patch('/update-number-info')
async def create_task(
	username: str = Body(embed=True),
	password: str = Body(embed=True),
	status: str = Body(embed=True),
	db: Session = Depends(get_db),
	form_data: model.OfficeTablePhoneNumberRequestForm = Depends(),
  	current_user: model.OfficeTableUserRequestForm = Depends(get_current_user)
):
	if current_user.username == username and current_user.password == password and current_user.status == status:
	
		db_number = db.query(model.OfficeTablePhoneNumber).filter_by(
			phone_number=form_data.phone_number
		).first()
	
		
		if db_number:
			if form_data.phone_info:
				db_number.phone_info = form_data.phone_info
			if form_data.is_active is not None:
				db_number.is_active = form_data.is_active
			if form_data.used is not None:
				db_number.used = form_data.used
			if form_data.missed is not None:
				db_number.missed = form_data.missed
			if form_data.processed is not None:
				db_number.processed = form_data.processed
			if form_data.recall is not None:
				db_number.recall = form_data.recall
			if form_data.decline is not None:
				db_number.decline = form_data.decline
			if form_data.recall_time:
				db_number.recall_time = form_data.recall_time
			if form_data.done_number_datetime:
				db_number.done_number_datetime = form_data.done_number_datetime
	
			db.commit()
			db.refresh(db_number)
			return {"number": db_number}
		else:
			return {"error": "Phone number dont found"}
	else:
		raise HTTPException(status_code=311, detail="Error user data")