from pydantic import BaseModel, Field
from typing import List, Optional, Generic, TypeVar
from pydantic.generics import GenericModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str
