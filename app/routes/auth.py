from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, models, database

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login')
async def login(user_credential: OAuth2PasswordRequestForm = Depends()):
    pass