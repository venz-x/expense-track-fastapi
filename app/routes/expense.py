from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, models, database, oauth2


router = APIRouter(
    tags=["Expense"]
)

@router.post('/expense', response_model=schemas.Expense)
async def expense_create(expense: schemas.ExpenseCreate, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    new_expense = models.Expense(owner_id = current_user.id, **expense.model_dump())

    db.add(new_expense)
    
    await db.commit()
    await db.refresh(new_expense)

    return new_expense

@router.get("/expense", response_model=list[schemas.ExpenseWithCategory])
async def get_all_expenses(db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    query = (select(models.Expense)
                    .where(models.Expense.owner_id == current_user.id)
                    .options(selectinload(models.Expense.category))
    )

    result = await db.execute(query)
    all_expenses = result.scalars().all()

    return all_expenses