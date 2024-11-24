# from typing import tuple
from fastapi import FastAPI
from decimal import Decimal
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
import models
import schemas
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from database import get_db, engine
from utils import get_env_variable


OPENAI_API_KEY = get_env_variable("OPENAI_API_KEY")


categories = [
    "Housing",
    "Transportation",
    "Food",
    "Utilities",
    "Insurance",
    "Medical/Healthcare",
    "Savings",
    "Debt",
    "Education",
    "Entertainment",
]

app = FastAPI()


def create_db_and_tables():
    models.Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/", response_model=schemas.Expenses)
async def create_expenses(
    expenses: schemas.CreateExpenses, db: Session = Depends(get_db)
):

    users_query = db.query(models.User).filter(models.User.telegram_id == expenses.telegram_id)
    user = users_query.first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    an_expenses = schemas.Expenses(
        user_id=user.id,
    )

    an_expenses.category, an_expenses.amount, an_expenses.description = (
        get_category_from_messages(expenses.message)
    )
    if an_expenses.category not in categories:
        raise HTTPException(status_code=400, detail="Invalid category")

    new_expenses = models.Expenses(**an_expenses.dict())
    db.add(new_expenses)
    db.commit()
    db.refresh(new_expenses)
    new_expenses.amount = Decimal(new_expenses.amount.replace("$", "").replace(",", ""))
    return new_expenses


def get_category_from_messages(message: str) -> tuple[str, Decimal, str]:
    template = """Select the category that best describes the following expense,
    and provide the price and a description. Only return the category name,
    the price and the description. For example, "Food, 10.00, I bought a sandwich." :
    {categories}

    message: {message}
    """

    prompt = ChatPromptTemplate.from_template(template)
    model = ChatOpenAI(model_name="gpt-4o-mini")
    chain = prompt | model | StrOutputParser()

    input_data = {"categories": categories, "message": message}

    category_price_description = chain.invoke(input_data)
    if not category_price_description:
        raise HTTPException(status_code=400, detail="Invalid message")

    category = category_price_description.split(",")[0].strip()
    price = category_price_description.split(",")[1].strip()
    description = category_price_description.split(",")[2].strip()
    return category, Decimal(price), description
