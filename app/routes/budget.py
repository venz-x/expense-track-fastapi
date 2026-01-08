from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from .. import schemas, models
from ..deps import DB, CurrentUser


router = APIRouter(
    tags=["Budget"]
)

# Set a budget for A category
@router.post("/budget/{id}", response_model=schemas.Budget)
async def create_budget(id: int, budget: schemas.BudgetCreate, db: DB, current_user: CurrentUser):
    query = (select(models.Budget)
                        .where(models.Budget.owner_id == current_user.id,
                            models.Budget.category_id == id
                        )
    )

    result = await db.execute(query)
    budget_exist = result.scalar()

    if budget_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Budget already exists for this category. Use Update instead.")

    new_budget = models.Budget(
        amount = budget.amount,
        owner_id = current_user.id,
        category_id = id,
    )

    db.add(new_budget)

    await db.commit()
    await db.refresh(new_budget)

    return new_budget

@router.get("/budget/{id}", response_model=schemas.Budget)
async def get_budget(id: int, db: DB, current_user: CurrentUser):
    query = (select(models.Budget)
                        .where(models.Budget.category_id == id,
                               models.Budget.owner_id == current_user.id
                        )
    )

    result = await db.execute(query)
    data = result.scalar()

    return data

@router.put("/budget/{id}", response_model=schemas.Budget)
async def update_budget(id: int, budget: schemas.BudgetUpdate, db: DB, current_user: CurrentUser):
    query = (select(models.Budget)
                        .where(models.Budget.category_id == id,
                                models.Budget.owner_id == current_user.id
                        )
    )

    result = await db.execute(query)
    budget_to_update = result.scalar()

    if budget_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Budget with category id {id} not found")
    
    budget_to_update.amount = budget.amount

    await db.commit()
    await db.refresh(budget_to_update)

    return budget_to_update