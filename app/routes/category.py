from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, models, database


router = APIRouter(
    tags=["Category"]
)

@router.post('/category', response_model=schemas.Category)
async def category_create(category: schemas.CategoryCreate, db: AsyncSession = Depends(database.get_db)):
    new_category = models.Category(**category.model_dump())

    db.add(new_category)

    await db.commit()
    await db.refresh(new_category)

    return new_category