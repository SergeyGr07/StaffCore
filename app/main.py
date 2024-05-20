import os
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from app import crud, models, schemas
from app.database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="app/templates")

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

def get_db(request: Request):
    return request.state.db

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    employees = crud.get_employees(db)
    return templates.TemplateResponse("index.html", {"request": request, "employees": employees})

@app.post("/employees/", response_class=HTMLResponse)
async def create_employee(request: Request, employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    crud.create_employee(db=db, employee=employee)
    employees = crud.get_employees(db)
    return templates.TemplateResponse("index.html", {"request": request, "employees": employees})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
