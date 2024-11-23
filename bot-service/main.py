from fastapi import FastAPI
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter
import models
import schemas
from database import get_db, engine

app = FastAPI()

def create_db_and_tables():
    models.Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post('/', response_model=schemas.CreateExpenses)
async def create_expenses(expenses:schemas.CreateExpenses, db:Session = Depends(get_db)):
    import pdb; pdb.set_trace()
    return {"message": f"Hello"}
