from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from .. import schemas, models
from ..deps import DB, CurrentUser


router = APIRouter(
    tags=["Analytics"]
)

# total amount sum
@router.get("/calculate_amount")
async def get_category_breakdown(db: DB, current_user: CurrentUser):
    query = (select(models.Category.name.label("category_name"), func.sum(models.Expense.amount).label("total_amount"))
                        .join(models.Category, models.Category.id == models.Expense.category_id)
                        .where(models.Expense.owner_id == current_user.id)
                        .group_by(models.Category.name)
    )

    result = await db.execute(query)
    data = result.mappings().all()

    return data
