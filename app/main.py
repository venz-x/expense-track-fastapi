from fastapi import FastAPI
from .routes import category, expense

app = FastAPI()


app.include_router(category.router)
app.include_router(expense.router)
