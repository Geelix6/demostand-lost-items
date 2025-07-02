import enum
import uuid
from models.db import Base
from sqlalchemy import Column, String, Enum as Enum
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from pgvector.sqlalchemy import Vector

class Location(enum.Enum):
    wagon = "в вагоне"
    station = "на станции"


class Item(Base):
    __tablename__ = "items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    date_lost = Column(
        TIMESTAMP(timezone=False, precision=3),
        nullable=False,
    )
    station = Column(
        String(length=63),
        nullable=False,
    )
    description = Column(
        String(length=4095),
        nullable=False
    )
    location = Column(
        Enum(Location, name="location_enum"),
        nullable=False
    )
    embedding = Column(
        Vector(384),
        nullable=True,
    )
