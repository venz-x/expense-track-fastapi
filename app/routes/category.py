from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .. import schemas, models
from ..deps import DB, CurrentUser

router = APIRouter(
    tags=["Category"]
)

@router.post('/category', response_model=schemas.Category)
async def category_create(category: schemas.CategoryCreate, db: DB, current_user: CurrentUser):
    new_category = models.Category(owner_id = current_user.id, **category.model_dump())

    db.add(new_category)

    await db.commit()
    await db.refresh(new_category)

    return new_category

@router.get('/category', response_model=schemas.Category)
async def get_categories(db: DB, current_user: CurrentUser):
    query = (select(models.Category)
                        .where(models.Category.owner_id == current_user.id)
                        .options(selectinload(models.Category.owner))        
    )

    result = await db.execute(query)
    category_data = result.scalar_one_or_none()

    if category_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Category data not found")

    return category_data

# all category and expenses
@router.get('/category_expenses', response_model=list[schemas.CategoryWithExpenses])
async def get_categories_expenses(db: DB, current_user: CurrentUser):
    query = (select(models.Category)
                        .where(models.Category.owner_id == current_user.id)
                        .options(selectinload(models.Category.expenses))
    )

    result = await db.execute(query)
    category_expense_data = result.scalars().all()

    return category_expense_data

# specific category ad expenses
@router.get("/category/{id}/expense", response_model=list[schemas.Expense])
async def get_category_expenses(id: int, db: DB, current_user: CurrentUser):
    query = (select(models.Expense)
                        .where(models.Expense.owner_id == current_user.id)
                        .where(models.Expense.category_id == id)
    )

    result = await db.execute(query)
    expenses = result.scalars().all()

    return expenses

@router.delete("/category/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(id: int, db: DB, current_user: CurrentUser):
    query = (select(models.Category)
                        .where(models.Category.owner_id == current_user.id,
                            models.Category.id == id       
                        )
    )

    result = await db.execute(query)
    category_to_delete = result.scalar()

    if category_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Category with id {id} not found")
    
    await db.delete(category_to_delete);
    await db.commit()

    return None

@router.patch("/category/{id}", response_model=schemas.Category)
async def update_category(id: int, category_update: schemas.CategoryUpdate, db: DB, current_user: CurrentUser):
    query = (select(models.Category)
                        .where(models.Category.id == id,
                               models.Category.owner_id == current_user.id
                        )
    )

    result = await db.execute(query)
    category_to_update = result.scalar()

    # The Pydantic model 'category_update' received from the API:
    # category_update = CategoryUpdate(name="New Food")

    if category_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Category with id {id} not found")
    
    updated_data = category_update.model_dump(exclude_unset=True)

    # Pydantic model converted into a standard Python dictionary.
    # 'exclude_unset=True' removed any null fields the user didn't send.
    # update_data is now:  {'name': 'New Food'}


    # Python calls .items() on the dictionary:
    # It creates a list of pairs: [ ('name', 'New Food') ]

    for key, value in updated_data.items():
        setattr(category_to_update, key, value)

    await db.commit()
    await db.refresh(category_to_update)

    return category_to_update