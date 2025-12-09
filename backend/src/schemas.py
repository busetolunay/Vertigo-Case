from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ClanBase(BaseModel): 
    name: str
    region: str

class ClanCreate(ClanBase): #POST
    pass

class ClanResponse(ClanBase): #GET
    id: UUID
    created_at: datetime

    class Config:  # to return sqlalchemy models to pydantic models
        from_attributes = True