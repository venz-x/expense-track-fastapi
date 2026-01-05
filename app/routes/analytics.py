from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, models, database, oauth2


router = APIRouter(
    tags=["Analytics"]
)