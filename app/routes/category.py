from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, models, database, oauth2


router = APIRouter(
    tags=["Category"]
)

@router.post('/category', response_model=schemas.Category)
async def category_create(category: schemas.CategoryCreate, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    new_category = models.Category(owner_id = current_user.id, **category.model_dump())

    db.add(new_category)

    await db.commit()
    await db.refresh(new_category)

    return new_category

@router.get('/category', response_model=schemas.Category)
async def get_categories(db: AsyncSession = Depends(database.get_db), curent_user: models.User = Depends(oauth2.get_current_user)):
    query = (select(models.Category)
                        .where(models.Category.owner_id == curent_user.id)
                        .options(selectinload(models.Category.owner))        
    )

    result = await db.execute(query)
    category_data = result.scalar_one_or_none()

    return category_data

# all category and expenses
@router.get('/category_expenses', response_model=list[schemas.CategoryWithExpenses])
async def get_categories_expenses(db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    query = (select(models.Category)
                        .where(models.Category.owner_id == current_user.id)
                        .options(selectinload(models.Category.expenses))
    )

    result = await db.execute(query)
    category_expense_data = result.scalars().all()

    return category_expense_data

# specific category ad expenses
@router.get("/category/{id}/expense", response_model=list[schemas.Expense])
async def get_category_expenses(id: int, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    query = (select(models.Expense)
                        .where(models.Expense.owner_id == current_user.id)
                        .where(models.Expense.category_id == id)
    )

    result = await db.execute(query)
    expenses = result.scalars().all()

    return expenses