from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, models, database, utils, oauth2

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login')
async def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(database.get_db)):
    query = (select(models.User)
                .where(models.User.email == user_credential.username)         
    )

    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credential")

    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credential")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }