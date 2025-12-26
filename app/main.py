from fastapi import FastAPI
from .routes import category, expense, user, auth

app = FastAPI()


app.include_router(category.router)
app.include_router(expense.router)
app.include_router(user.router)
app.include_router(auth.router)
