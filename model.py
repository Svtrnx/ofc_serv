from sqlalchemy import Column, Integer, String, DateTime, Boolean, Numeric
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Form

Base = declarative_base()


class OfficeTableUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    balance = Column(Numeric(10, 2), default=0.00)
    status = Column(String)
    hwid = Column(String)
    language = Column(String)
    
class OfficeTableUserRequestForm:
	
    def __init__(
        self,
        username: str = Form(),
        password: str = Form(),
        balance: float = Form(),
        status: str = Form(),
        hwid: str = Form(),
        language: str = Form(),
    ):
        self.username = username
        self.password = password
        self.balance = balance
        self.status = status
        self.hwid = hwid
        self.language = language
        

class OfficeTableUserShortRequestForm:
	
    def __init__(
        self,
        username: str = Form(),
        password: str = Form(),
        status: str = Form(),
        hwid: str = Form(),
        language: str = Form(),
    ):
        self.username = username
        self.password = password
        self.status = status
        self.hwid = hwid
        self.language = language
    
    
class OAuth2PasswordRequestFormSignin:
	
    def __init__(
        self,
        username: str = Form(),
        password: str = Form(),
    ):
        self.username = username
        self.password = password
