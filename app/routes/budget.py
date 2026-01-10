from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from .. import schemas, models
from ..deps import DB, CurrentUser


router = APIRouter(
    tags=["Budget"]
)

# Set a budget for A category
@router.post("/budget/{id}", response_model=schemas.BudgetWithCategory)
async def create_budget(id: int, budget: schemas.BudgetCreate, db: DB, current_user: CurrentUser):
    category_query = (select(models.Category)
                                .where(models.Category.id == id,
                                        models.Category.owner_id == current_user.id
                                )
    )

    result = await db.execute(category_query)
    category_result = result.scalar()

    if category_result is None:
        raise HTTPException(status_code=404, detail="Category not found")

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

    new_budget.category = category_result

    return new_budget

@router.get("/budget/{id}", response_model=schemas.BudgetWithCategory)
async def get_budget(id: int, db: DB, current_user: CurrentUser):
    query = (select(models.Budget)
                        .where(models.Budget.category_id == id,
                               models.Budget.owner_id == current_user.id
                        )
                        .options(selectinload(models.Budget.category))
    )

    result = await db.execute(query)
    data = result.scalar()

    if not data:
        raise HTTPException(status_code=404, detail="Budget not found")

    return data

@router.put("/budget/{id}", response_model=schemas.BudgetWithCategory)
async def update_budget(id: int, budget: schemas.BudgetUpdate, db: DB, current_user: CurrentUser):
    query = (select(models.Budget)
                        .where(models.Budget.category_id == id,
                                models.Budget.owner_id == current_user.id
                        )
                        .options(selectinload(models.Budget.category))
    )

    result = await db.execute(query)
    budget_to_update = result.scalar()

    if budget_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Budget with category id {id} not found")
    
    budget_to_update.amount = budget.amount

    await db.commit()
    # await db.refresh(budget_to_update) --> not using the refresh as it will remove the selectinloads category relation data

    return budget_to_update

# delete by category id
@router.delete("/budget/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget(id: int, db: DB, current_user: CurrentUser):
    query = (select(models.Budget)
                        .where(models.Budget.category_id == id,
                            models.Budget.owner_id == current_user.id
                        )
    )

    result = await db.execute(query)
    budget_to_delete = result.scalar()

    if budget_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Category budget with id {id} not found")
    
    await db.delete(budget_to_delete)
    await db.commit()

    return None