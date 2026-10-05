from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.datascience import ds_models

class DSRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_file_upload(self, file_upload: ds_models.DsFileUploads) -> ds_models.DsFileUploads:
        self.db.add(file_upload)
        await self.db.commit()
        await self.db.refresh(file_upload)
        return file_upload

    async def get_file_upload_by_id(self,id: int) -> ds_models.DsFileUploads:
        result = await self.db.execute(select(ds_models.DsFileUploads).where(ds_models.DsFileUploads.id ==id))
        return result.scalar_one_or_none()

    async def update_file_upload(self, file_upload: ds_models.DsFileUploads) -> ds_models.DsFileUploads:
        await self.db.merge(file_upload)
        await self.db.commit()
        await self.db.refresh(file_upload)
        return file_upload