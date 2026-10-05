from asgiref.sync import async_to_sync

from src.utile.celery_conf import celery_app
from src.datascience.ds_repository import DSRepository
from database import SessionLocal
from src.utile.aws import S3
import csv
import io

s3 = S3()
CHUNK_SIZE = 100 * 1024 * 1024  # 100 MB
from .models import EcommerceRepository


def process_csv_chunk(data: bytes):
    csv_file = io.StringIO(
        data.decode("utf-8")
    )
    reader = csv.reader(csv_file)
    rows = []
    repository = EcommerceRepository()
    try:
        for row in reader:
            if not row:
                continue
            rows.append(row)
            if len(rows) >= 10_000:
                repository.bulk_insert(rows)
                rows.clear()
        if rows:
            repository.bulk_insert(rows)
    except Exception as e:
        print(e)
    


async def process_file_upload(file_id: int):

    async with SessionLocal() as db:

        ds_repo = DSRepository(db)

        file_upload = await ds_repo.get_file_upload_by_id(file_id)

        if file_upload is None:
            raise Exception(f"File ID {file_id} not found")

        return file_upload

@celery_app.task(name="fs_csv_file_convert_db", bind=True, max_retries=3, default_retry_delay=60)
def csv_file_convert_db(self,file_id:int):
        
    try:
        # print("========== SELF ==========")
        # print(self)

        # print("========== DIR(SELF) ==========")
        # print(dir(self))

        # print("========== SELF DICT ==========")
        # print(self.__dict__)

        # print("========== REQUEST ==========")
        # print(self.request)

        # print("========== REQUEST DICT ==========")
        # print(self.request.__dict__)

        file_upload = async_to_sync(process_file_upload)(file_id)        
        stream = s3.get_object(file_upload.file_path)
        buffer = b""
        while True:

            # Read 100 MB S3 chunk
            chunk = stream.read(CHUNK_SIZE)

            if not chunk:
                break

            # Add new bytes to previous incomplete data
            buffer += chunk

            # Find the last newline
            last_newline = buffer.rfind(b"\n")

            if last_newline == -1:
                # No complete CSV row yet
                continue

            # Complete CSV data
            complete_data = buffer[:last_newline + 1]

            # Keep incomplete row for next iteration
            buffer = buffer[last_newline + 1:]
            process_csv_chunk(complete_data)

        # Process remaining data
        if buffer:
            process_csv_chunk(buffer)

        stream.close()

        return f"File '{file_id}' successfully processed."

    except Exception as e:
        return f"Failed to upload file '{file_id}' to '{file_id}': {str(e)}"