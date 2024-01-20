from sqlalchemy import Column, Integer, String, DateTime, Boolean, Numeric
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Form
from datetime import datetime

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
    
    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "balance": float(self.balance),  # Convert Numeric to float
            "status": self.status,
            "hwid": self.hwid,
            "language": self.language
        }
    
class OfficeTablePhoneNumber(Base):
    __tablename__ = 'phone_numbers'

    id = Column(Integer, primary_key=True)
    phone_number = Column(String)
    phone_info = Column(String)
    is_active = Column(Boolean)
    used = Column(Boolean)
    missed = Column(Boolean)
    processed = Column(Boolean)
    recall = Column(Boolean)
    decline = Column(Boolean)
    phone_datetime = Column(DateTime)
    recall_time = Column(DateTime)
    done_number_datetime = Column(DateTime)


class OfficeTablePc(Base):
    __tablename__ = 'pc'

    id = Column(Integer, primary_key=True)
    hwid = Column(String)
    pc_name = Column(String)
    activated = Column(DateTime)
    
class OfficeTableKey(Base):
    __tablename__ = 'keys'

    id = Column(Integer, primary_key=True)
    soft_key = Column(String)
  
class OfficeTablePromocodes(Base):
    __tablename__ = 'promos'

    id = Column(Integer, primary_key=True)
    promocode = Column(String)
    username = Column(String)
    promo_datetime = Column(DateTime)
    
  
class OfficeTableLog(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    log_info = Column(String)
    username = Column(String)
    log_datetime = Column(DateTime)
    

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