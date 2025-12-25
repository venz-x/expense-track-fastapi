from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from . import database, models, schemas

app = FastAPI()

@app.post('/category', response_model=schemas.Category)
async def category_create(category: schemas.CategoryCreate, db: AsyncSession = Depends(database.get_db)):
    new_category = models.Category(**category.model_dump())

    db.add(new_category)

    await db.commit()
    await db.refresh(new_category)

    return new_category

@app.post('/expense', response_model=schemas.Expense)
async def expense_create(expense: schemas.ExpenseCreate, db: AsyncSession = Depends(database.get_db)):
    new_expense = models.Expense(**expense.model_dump())

    db.add(new_expense)
    
    await db.commit()
    await db.refresh(new_expense)

    return new_expense

