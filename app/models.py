from pydantic import BaseModel, ValidationError, validator
from typing import Dict, Optional, Union

class AccountBase(BaseModel):
    name: str = ''
    description: Optional[str] = None
    balance: float = 0.0
    active: bool = True

    @validator('name')
    def name_alphanumeric(cls, v):
        assert v.isalnum() or v == '', 'must be alphanumeric'
        return v

class Account(AccountBase):
    id: int
