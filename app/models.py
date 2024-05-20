from sqlalchemy import Column, Integer, String
from .database import Base

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    position = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    tg = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    weaknesses = Column(String)
    strengths = Column(String)
