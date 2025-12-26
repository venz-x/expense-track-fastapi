from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import schemas, models, database, utils

router = APIRouter(
    tags=["User"]
)

@router.post('/users', response_model=schemas.User)
async def user_create(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    new_user = models.User(**user.model_dump())

    hash_pass = utils.hash(new_user.password)

    new_user.password = hash_pass
    
    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user