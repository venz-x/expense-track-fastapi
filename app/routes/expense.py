from fastapi import APIRouter, Depends, status, HTTPException
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

@router.get("/expense/{id}", response_model=schemas.Expense)
async def delete_expense(id: int, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    query = (select(models.Expense)
                        .where(models.Expense.id == id,
                               models.Expense.owner_id == current_user.id
                        )
    )

    result = await db.execute(query)
    expense = result.scalar_one_or_none()

    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Expense with id {id} not found")

    return expense

@router.delete("/expense/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(id: int, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    query = (select(models.Expense)
                        .where(models.Expense.id == id,
                               models.Expense.owner_id == current_user.id
                        )
    )

    result = await db.execute(query)
    expense_to_delete = result.scalar()

    if expense_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Expense with id {id} not found")
    
    await db.delete(expense_to_delete)
    await db.commit()

    return None