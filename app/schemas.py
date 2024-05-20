from pydantic import BaseModel

class EmployeeBase(BaseModel):
    name: str
    position: str
    phone: str
    tg: str
    email: str
    weaknesses: str
    strengths: str

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True
