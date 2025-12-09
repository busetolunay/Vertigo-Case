import uuid
import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

class Clan(Base):
    __tablename__ = "clans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid.uuid4())) # UUID primary key
    name = Column(String, nullable=False)
    region = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))