from pydantic import BaseModel,EmailStr,Field,validator,ConfigDict,constr,field_validator
from typing import Optional


class FileUpload(BaseModel):
    file_name: str = Field(..., max_length=50, examples=["data.csv"])
    file_content_type: Optional[str] = Field(default=None, examples=["text/csv"])

class FileUploadResponse(BaseModel):
    id: int
    file_name: str 
    file_path: str
    presigned_url: str

    model_config = ConfigDict(from_attributes=True)

class FileUploadStatusResponse(BaseModel):
    file_name: str 
    file_path: str

    model_config = ConfigDict(from_attributes=True)

class kafkaMessage(BaseModel):
    id:int
    file_path: str

    model_config = ConfigDict(from_attributes=True)