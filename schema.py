from pydantic import BaseModel, Field
from typing import List, Optional, Generic, TypeVar
from pydantic.generics import GenericModel
from datetime import datetime


class OfficePcSchema(BaseModel):
    id: int
    hwid: Optional[str]=None
    pc_name: Optional[str]=None
    activated: Optional[datetime]=None

class Token(BaseModel):
    access_token: str
    token_type: str
