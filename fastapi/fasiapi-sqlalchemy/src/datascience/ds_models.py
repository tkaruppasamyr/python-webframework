from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, Numeric, TIMESTAMP, func
from sqlalchemy.orm import relationship     
from datetime import datetime

class DsFileUploads(Base):

    __tablename__ = "ds_fileuploads"

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    file_name = Column(String(50),index=True,nullable=False)
    file_path = Column(String(255),nullable=False)
    uploaded_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    upload_status = Column(String(50),nullable=False,default="pending")
    prediction_status = Column(String(50),nullable=False,default="pending")
    is_active = Column(Boolean(),default=True,nullable=False)
    convert_db = Column(String(50),nullable=True,default="pending")
