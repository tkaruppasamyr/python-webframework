from fastapi import APIRouter, status, Depends, HTTPException
from src.utile.aws import S3
from src.datascience import ds_schema
from src.datascience.ds_depedencies import file_upload_depends
from src.datascience.ds_service import DSService
from src.utile.celery_conf import celery_app
from src.fileupload import fs_schema
from .fs_tasks import csv_file_convert_db

fs_router = APIRouter(
    prefix="/fileupload",
    tags=["fileupload"],
    responses={404: {"description": "Not found"}},
)

s3 = S3()

@fs_router.post("/upload",response_model=ds_schema.FileUploadResponse, status_code=status.HTTP_200_OK)
async def upload_file(file_details: ds_schema.FileUpload,ds_service: DSService = Depends(file_upload_depends)):
    try:
        result = await ds_service.create_file_upload(file_details,foldername="fileupload")
        presigned_url = S3().put_object_presigned_url(result.file_path, content_type=file_details.file_content_type)

        print(f"File ID: {result.id}")
        print(f"File path: {result.file_path}")
        print(f"Presigned URL: {presigned_url}")

        response = ds_schema.FileUploadResponse(
            id=result.id,
            file_name=result.file_name,
            file_path=result.file_path,
            presigned_url=presigned_url
        )

        return response
    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}


@fs_router.post("/{file_upload_id}/file-upload-status", status_code=status.HTTP_200_OK)
async def get_file_upload_status(file_upload_id: int, fileup_schema: ds_schema.FileUploadStatusResponse, 
                                 ds_service: DSService = Depends(file_upload_depends)):
    try:
        # print(f"File ID: {file_upload_id}")
        # print(f"File name: {fileup_schema.file_name}")
        # print(f"File path: {fileup_schema.file_path}")

        result = await ds_service.update_file_status(file_upload_id,fileup_schema)
        print(f"Updated File ID: {result.id}")
        csv_file_convert_db.delay(result.id)
        
        return {"file_name": "hello", "file_path": "update"}
    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}

@fs_router.get("/celery-status",response_model=fs_schema.CeleryStatusResponse, status_code=status.HTTP_200_OK)
async def get_celery_status():

    # add_numbers.delay(1, 2)  # Example task to demonstrate Celery functionality
    try:
        inspect = celery_app.control.inspect()

        active = inspect.active() or {}
        scheduled = inspect.scheduled() or {}
        reserved = inspect.reserved() or {}

        active_tasks = []
        pending_tasks = []
        scheduled_tasks = []

        # Active
        for worker, tasks in active.items():
            for task in tasks:
                active_tasks.append({
                    "worker": worker,
                    "task_id": task.get("id"),
                    "task_name": task.get("name"),
                    "args": task.get("args"),
                    "kwargs": task.get("kwargs"),
                    "time_start": task.get("time_start"),
                })

        # Pending / Reserved
        for worker, tasks in reserved.items():
            for task in tasks:
                pending_tasks.append({
                    "worker": worker,
                    "task_id": task.get("id"),
                    "task_name": task.get("name"),
                    "args": task.get("args"),
                    "kwargs": task.get("kwargs"),
                    "time_start": None,
                })

        # Scheduled
        for worker, tasks in scheduled.items():
            for task in tasks:
                request = task.get("request", {})

                scheduled_tasks.append({
                    "worker": worker,
                    "task_id": request.get("id"),
                    "task_name": request.get("name"),
                    "args": request.get("args"),
                    "kwargs": request.get("kwargs"),
                    "time_start": None,
                })

        return {
            "active": {
                "count": len(active_tasks),
                "tasks": active_tasks,
            },
            "pending": {
                "count": len(pending_tasks),
                "tasks": pending_tasks,
            },
            "scheduled": {
                "count": len(scheduled_tasks),
                "tasks": scheduled_tasks,
            },
        }
    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}