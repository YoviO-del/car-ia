import uuid

from sqlalchemy import Column, Integer, String, DateTime, JSON, text
from sqlalchemy.sql import func
from database import Base


class Profile(Base):
    __tablename__ = "profile_information"  # change to your actual table name

    # char(36) PK, holds LINKEDIN id from simple login feature
    id = Column(String(36), primary_key=True, autoincrement=False)

    profile_name = Column(String(255), nullable=True)

    # JSON NOT NULL, default {"reports": []}
    report_JSON = Column(
        JSON,
        nullable=False,
        default=lambda: {"reports": []},
        server_default=text("(json_object('reports', json_array()))"),
    )

    overall_score = Column(Integer, nullable=True)

    created_at = Column(
        DateTime,
        nullable=True,
        server_default=func.now(),
    )