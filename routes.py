
from fastapi import Depends, APIRouter, Request, Body, Response, HTTPException, status, Form, Cookie
from sqlalchemy.orm import Session
from connection import session, get_db, get_current_user
from schema import Token
import model
import userController
from datetime import timedelta, datetime
from dotenv import load_dotenv
from starlette.responses import RedirectResponse
from authSecurity import get_current_user, create_access_token
from config import ACCESS_TOKEN_EXPIRE_MINUTES, COOKIE_NAME

load_dotenv()
userRouter = APIRouter()

@userRouter.get("/index")
def get_index(request: Request):
	return {"request": request.url}

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

# @userRouter.get('/get-user')
# def get_user(username: str, db: Session = Depends(get_db), current_user: model.OfficeTableUserRequestForm = Depends(get_current_user)):
# 	if current_user.username == username:
# 		user = get_current_user(username)
# 		if user:
# 			return {"user": user}
# 		else:
# 			raise HTTPException(status_code=309, detail="Dont found user")
# 	else:
# 		raise HTTPException(status_code=310, detail="Error to authenticate")
@userRouter.get('/get-user')
def get_user(db: Session = Depends(get_db), current_user: model.OfficeTableUserRequestForm = Depends(get_current_user)):
	user = current_user
	return user

@userRouter.patch('/update-user-info')
async def create_task(
	username: str = Body(embed=True),
	password: str = Body(embed=True),
	status: str = Body(embed=True),
	hwid: str = Body(embed=True),
	language: str = Body(embed=True),
	db: Session = Depends(get_db),
	form_data: model.OfficeTableUserShortRequestForm = Depends(),
  	current_user: model.OfficeTableUserRequestForm = Depends(get_current_user)
):
	if current_user.username == username and current_user.password == password and current_user.status == status and current_user.hwid == hwid:
		form_data.username 	= username
		form_data.password 	= password
		form_data.status 	= status
		form_data.hwid 		= hwid
		form_data.language 	= language
		
		db_user = db.query(model.OfficeTableUser).filter_by(
			username=form_data.username,
			password=form_data.password,
			status=form_data.status,
			hwid=form_data.hwid,
		).first()
	
		
		if db_user:
			updated_rows = db.query(model.OfficeTableUser).filter_by(
				username=form_data.username,
				password=form_data.password,
				status=form_data.status,
				hwid=form_data.hwid,
			).update({"language": form_data.language})
			if updated_rows > 0:
				db.commit()
				return {
					"message": f"User has been updated successfully!"
				}
			else:
				return {"message": "No matching rows found for update"}
		else:
			return {"error": "Proxy dont found"}
	else:
		raise HTTPException(status_code=311, detail="Error user data")
