from fastapi import APIRouter,status, Depends, HTTPException
from src.utile.aws import S3
from src.datascience import ds_schema
from src.datascience.ds_service import DSService
from src.datascience.ds_depedencies import file_upload_depends
from starlette.concurrency import run_in_threadpool
from src.utile.kafka import KafkaService, get_kafka
ds_router = APIRouter(
    prefix="/datascience",
    tags=["datascience"],
    responses={404: {"description": "Not found"}},
)


@ds_router.post("/file-upload", response_model=ds_schema.FileUploadResponse,status_code=status.HTTP_200_OK)
async def employee_file_upload(file_details: ds_schema.FileUpload, ds_service: DSService = Depends(file_upload_depends)):
    try:
        result = await ds_service.create_file_upload(file_details,foldername="datascience")
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

@ds_router.post("/{file_upload_id}/file-upload-status", status_code=status.HTTP_200_OK)
async def get_file_upload_status(file_upload_id: int, fileup_schema: ds_schema.FileUploadStatusResponse, 
                                 kafka: KafkaService = Depends(get_kafka),ds_service: DSService = Depends(file_upload_depends)):
    try:
        print(f"File ID: {file_upload_id}")
        print(f"File name: {fileup_schema.file_name}")
        print(f"File path: {fileup_schema.file_path}")

        result = await ds_service.update_file_status(file_upload_id,fileup_schema)
        kafka_message = ds_schema.kafkaMessage.model_validate(result)
        print(f"Updated File ID: {kafka_message}")

        # kafka_service = KafkaService()
        # kafka_service.produce_message('file_upload_status', key=str(file_upload_id), value=kafka_message.model_dump_json().encode('utf-8'))
        await run_in_threadpool(kafka.produce_message, topic='file_upload_status', key=str(file_upload_id), value=kafka_message.model_dump_json().encode('utf-8'))
        return {"file_name": "hello", "file_path": "update"}
    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}    