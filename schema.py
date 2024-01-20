from pydantic import BaseModel, Field
from typing import List, Optional, Generic, TypeVar
from pydantic.generics import GenericModel
from datetime import datetime


class OfficePcSchema(BaseModel):
    id: int
    hwid: Optional[str]=None
    pc_name: Optional[str]=None
    activated: Optional[datetime]=None
    
class OfficeNumberSchema(BaseModel):
    id: int
    phone_number: Optional[str]=None
    is_active: Optional[bool]=None
    used: Optional[bool]=None
    missed: Optional[bool]=None
    processed: Optional[bool]=None
    recall: Optional[bool]=None
    decline: Optional[bool]=None
    phone_datetime: Optional[datetime]=None
    
class OfficeLogSchema(BaseModel):
    id: int
    log_info: Optional[str]=None
    username: Optional[str]=None
    log_datetime: Optional[datetime]=None

class Token(BaseModel):
    access_token: str
    token_type: str
