from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from .. import schemas, models
from ..deps import DB, CurrentUser


router = APIRouter(
    tags=["Analytics"]
)

# total amount sum of all category
@router.get("/calculate_amount_all")
async def get_category_breakdown(db: DB, current_user: CurrentUser):
    query = (select(func.sum(models.Expense.amount).label("total_amount"))
                    .where(models.Expense.owner_id == current_user.id)
    )

    result = await db.execute(query)
    data = result.mappings().first()

    return data

# total amount sum of all category individually
@router.get("/calculate_amount", response_model=list[schemas.CategoryBreakdown])
async def get_category_breakdown(db: DB, current_user: CurrentUser):
    # SELECT name FROM categories
    query = (select(models.Category.name.label("category_name"), func.sum(models.Expense.amount).label("total_amount"))
                        .join(models.Category, models.Category.id == models.Expense.category_id)
                        .where(models.Expense.owner_id == current_user.id)
                        .group_by(models.Category.name)
    )

    result = await db.execute(query)
    data = result.mappings().all()

    return data

# total amount sum of specific category
@router.get("/calculate_amount/{id}", response_model=schemas.CategoryBreakdown)
async def get_category_breakdown_by_id(id: int, db: DB, current_user: CurrentUser):
    query = (select(models.Category.name.label("category_name"), func.sum(models.Expense.amount).label("total_amount"))
                        .join(models.Category, models.Category.id == models.Expense.category_id)
                        .where(models.Category.id == id, models.Category.owner_id == current_user.id)
                        .group_by(models.Category.name)
    )

    result = await db.execute(query)
    data = result.mappings().first()

    if not data:
        raise HTTPException(status_code=404, detail="Category not found or has no expenses")

    return data