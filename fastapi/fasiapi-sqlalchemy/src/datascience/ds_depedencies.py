from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from src.datascience.ds_service import DSService
from src.datascience.ds_repository import DSRepository


def file_upload_depends(db: AsyncSession = Depends(get_db)) -> DSService:
    repo = DSRepository(db)
    return DSService(repo)