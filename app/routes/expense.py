from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, models, database


router = APIRouter(
    tags=["Expense"]
)

@router.post('/expense', response_model=schemas.Expense)
async def expense_create(expense: schemas.ExpenseCreate, db: AsyncSession = Depends(database.get_db)):
    new_expense = models.Expense(**expense.model_dump())

    db.add(new_expense)
    
    await db.commit()
    await db.refresh(new_expense)

    return new_expense