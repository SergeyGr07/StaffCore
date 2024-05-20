from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from . import models, schemas, crud
from .database import SessionLocal, engine, Base

app = FastAPI()

# Монтируем директорию static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Подключаем Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Создаем базу данных
Base.metadata.create_all(bind=engine)

# Получение сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    employees = crud.get_employees(db)
    return templates.TemplateResponse("index.html", {"request": request, "employees": employees})

@app.post("/employees/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = crud.create_employee(db, employee)
    return db_employee
