from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from .. import schemas, models
from ..deps import DB, CurrentUser


router = APIRouter(
    tags=["Expense"]
)

@router.post('/expense', response_model=schemas.Expense)
async def expense_create(expense: schemas.ExpenseCreate, db: DB, current_user: CurrentUser):
    new_expense = models.Expense(owner_id = current_user.id, **expense.model_dump())

    db.add(new_expense)
    
    await db.commit()
    await db.refresh(new_expense)

    return new_expense

@router.get("/expense", response_model=list[schemas.ExpenseWithCategory])
async def get_all_expenses(
        db: DB,
        current_user: CurrentUser,
        limit: int = 10,
        offset: int = 0,
        search: str | None = None
    ):

    query = (select(models.Expense)
                    .where(models.Expense.owner_id == current_user.id)
                    .options(selectinload(models.Expense.category))
    )

    if search:
        query = query.where(models.Expense.description.ilike(f"%{search}%"))
    
    query = (
        query
        .order_by(desc(models.Expense.date))
        .limit(limit)
        .offset(offset)
    )

    result = await db.execute(query)
    all_expenses = result.scalars().all()

    return all_expenses

@router.get("/expense/{id}", response_model=schemas.Expense)
async def delete_expense(id: int, db: DB, current_user: CurrentUser):
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
async def delete_expense(id: int, db: DB, current_user: CurrentUser):
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

@router.patch("/expense/{id}", response_model=schemas.ExpenseWithCategory)
async def update_expense(id: int, expense_update: schemas.ExpenseUpdate, db: DB, current_user: CurrentUser):
    query = (select(models.Expense)
                        .where(models.Expense.owner_id == current_user.id,
                               models.Expense.id == id
                        )
                        .options(selectinload(models.Expense.category))
    )

    result = await db.execute(query)
    expense_to_update = result.scalar()

    if expense_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Expense with id {id} not found")
    
    updated_data = expense_update.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(expense_to_update, key, value)
    
    await db.commit()
    await db.refresh(expense_to_update)

    return expense_to_update