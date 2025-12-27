from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, models, database

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login')
async def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(database.get_db)):
    query = (select(models.User)
                .where(models.User.email == user_credential.username)         
    )