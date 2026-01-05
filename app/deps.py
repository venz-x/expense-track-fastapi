from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from . import database, models, oauth2

DB = Annotated[AsyncSession, Depends(database.get_db)]

CurrentUser = Annotated[models.User, Depends(oauth2.get_current_user)]