from src.datascience import ds_schema, ds_models
from src.datascience.ds_models import DsFileUploads
from datetime import datetime
import uuid
from src.datascience.ds_repository import DSRepository

class DSService:

    def __init__(self, dsrepo: DSRepository):
        self.ds_repo = dsrepo


    async def create_file_upload(self, file_up_schema: ds_schema.FileUpload,foldername:str):

        original_fname = file_up_schema.file_name
        fname_ext = original_fname.split(".")[-1]
        ts_fname = datetime.now().strftime('%Y%m%d%H%M%S')
        random_fname = f"{uuid.uuid4().hex}.{fname_ext}"
        object_key = f"{foldername}/{ts_fname}/{random_fname}"

        file_upload = DsFileUploads(
            file_name=original_fname,
            file_path=object_key,
            upload_status="pending",
            prediction_status="pending",
            is_active=True,
            uploaded_at=datetime.now()
        )

        return await self.ds_repo.create_file_upload(file_upload)

    async def update_file_status(self, file_upload_id: int, fileup_schema: ds_schema.FileUploadStatusResponse):
        file_data = await self.ds_repo.get_file_upload_by_id(file_upload_id)
        if file_data is None:
            raise ValueError(f"File upload with ID {file_upload_id} not found.")

        if fileup_schema.file_name != file_data.file_name and fileup_schema.file_path != file_data.file_path:
            raise ValueError("File name and file path do not match the existing record.")

        # Update the upload_status on the existing file_data object
        file_data.upload_status = "completed"
        
        # return entire row object
        return await self.ds_repo.update_file_upload(file_data)

            
        
        
        
        