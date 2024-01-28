from sqlalchemy import Column, Integer, String, DateTime, Boolean, Numeric
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Form
from datetime import datetime

Base = declarative_base()


class OfficeTableUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True)
    password = Column(String, index=True)
    balance = Column(Numeric(10, 2), default=0.00, index=True)
    status = Column(String, index=True)
    hwid = Column(String, index=True)
    language = Column(String, index=True)
    reg_datetime = Column(DateTime, index=True)
    
    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "balance": float(self.balance),
            "status": self.status,
            "hwid": self.hwid,
            "language": self.language,
            "reg_datetime": self.reg_datetime
        }
    
class OfficeTablePhoneNumber(Base):
    __tablename__ = 'phone_numbers'

    id = Column(Integer, primary_key=True)
    phone_number = Column(String, index=True)
    phone_info = Column(String, index=True)
    user_work = Column(String, index=True)
    is_active = Column(Boolean, index=True)
    used = Column(Boolean, index=True)
    missed = Column(Boolean, index=True)
    processed = Column(Boolean, index=True)
    recall = Column(Boolean, index=True)
    decline = Column(Boolean, index=True)
    phone_datetime = Column(DateTime, index=True)
    recall_time = Column(DateTime, index=True)
    done_number_datetime = Column(DateTime, index=True)


class OfficeTablePc(Base):
    __tablename__ = 'pc'

    id = Column(Integer, primary_key=True)
    hwid = Column(String)
    pc_name = Column(String)
    activated = Column(DateTime)
    
class OfficeTableKey(Base):
    __tablename__ = 'keys'

    id = Column(Integer, primary_key=True)
    soft_key = Column(String, index=True)
  
class OfficeTablePromocodes(Base):
    __tablename__ = 'promos'

    id = Column(Integer, primary_key=True)
    promocode = Column(String, index=True)
    username = Column(String, index=True)
    promo_datetime = Column(DateTime, index=True)
    
  
class OfficeTableLog(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    log_info = Column(String, index=True)
    username = Column(String, index=True)
    log_datetime = Column(DateTime, index=True)
    

class OfficeTablePcRequestForm:
	
    def __init__(
        self,
        hwid: str = Form(),
        pc_name: str = Form(),
    ):
        self.hwid = hwid
        self.pc_name = pc_name
        
    
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
        status: str = Form(default=None),
        hwid: str = Form(default=None),
        language: str = Form(),
    ):
        self.username = username
        self.password = password
        self.status = status
        self.hwid = hwid
        self.language = language
        
class OfficeTableCreateUserRequestForm:
	
    def __init__(
        self,
        username: str = Form(),
        password: str = Form(),
        balance: int = Form(default=0),
        status: str = Form(),
        hwid: str = Form(default=None),
        language: str = Form(),
    ):
        self.username = username
        self.password = password
        self.balance = balance
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


class OfficeTablePhoneNumberRequestForm:
	
    def __init__(
        self,
        phone_number: str = Form(default=None),
        phone_info: str = Form(default=None),
        is_active: bool = Form(default=None),
        used: bool = Form(default=None),
        missed: bool = Form(default=None),
        processed: bool = Form(default=None),
        recall: bool = Form(default=None),
        decline: bool = Form(default=None),
        recall_time: datetime = Form(default=None),
        done_number_datetime: datetime = Form(default=None),
    ):
        self.phone_number = phone_number
        self.phone_info = phone_info
        self.is_active = is_active
        self.used = used
        self.missed = missed
        self.processed = processed
        self.recall = recall
        self.decline = decline
        self.recall_time = recall_time
        self.done_number_datetime = done_number_datetime