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
    created_at:Optional[datetime] = datetime # default to now

    class Config:  # to configure Pydantic model to work with ORM objects returned by SQLAlchemy
        from_attributes = True