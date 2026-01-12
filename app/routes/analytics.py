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
async def get_all_category_breakdown(db: DB, current_user: CurrentUser):
    query = (select(func.sum(models.Expense.amount).label("total_amount"))
                    .where(models.Expense.owner_id == current_user.id)
    )

    result = await db.execute(query)
    data = result.mappings().first()

    return data

# total amount sum of all category individually
@router.get("/analytics", response_model=list[schemas.CategoryBreakdown])
async def get_total_category_sum(db: DB, current_user: CurrentUser):
    # SELECT name FROM categories
    query = (select(models.Category.name.label("category_name"), func.sum(models.Expense.amount).label("total_amount"))
                        .join(models.Category, models.Category.id == models.Expense.category_id)
                        .where(models.Expense.owner_id == current_user.id)
                        .group_by(models.Category.name)
    )

    result = await db.execute(query)
    data = result.mappings().all()

    return data

# Working here
@router.get("/analytics/status", response_model=list[schemas.BudgetStatusWithCategory])
async def get_budget_status(db: DB, current_user: CurrentUser):
    query = (select(models.Budget, func.coalesce(func.sum(models.Expense.amount), 0).label("spend"))
                        .outerjoin(models.Expense, models.Budget.category_id == models.Expense.category_id)
                        .where(models.Budget.owner_id == current_user.id)
                        .group_by(models.Budget.id)
                        .options(selectinload(models.Budget.category))
    )
    
    result = await db.execute(query)
    status = result.all() # scalars() give BudgetObject, BudgetObject from [(BudgetObject, 500), (BudgetObject, 1500)].
                          # all() gives a list of tuple [(BudgetObject, 500), (BudgetObject, 1500)]

    
    if status is None:
        if not status:
            raise HTTPException(status_code=404, detail="Category not found or has no budget")
    
    data = []
    for budget, spend in status:
        remaining = budget.amount - spend

        status_label = "Over Budget" if remaining < 0 else "Good"

        # inside data[i]  -> e.g data[0]
        data.append(schemas.BudgetStatusWithCategory(
            amount = budget.amount,
            spend = spend,
            remaining = remaining,
            status = status_label,
            category = budget.category
        ))
    
    return data

# total amount sum of specific category
@router.get("/analytics/{category_id}", response_model=schemas.CategoryBreakdown)
async def get_category_breakdown_by_id(category_id: int, db: DB, current_user: CurrentUser):
    query = (select(models.Category.name.label("category_name"), func.sum(models.Expense.amount).label("total_amount"))
                        .join(models.Category, models.Category.id == models.Expense.category_id)
                        .where(models.Category.id == category_id, models.Category.owner_id == current_user.id)
                        .group_by(models.Category.name)
    )

    result = await db.execute(query)
    data = result.mappings().first()

    if not data:
        raise HTTPException(status_code=404, detail="Category not found or has no expenses")

    return data