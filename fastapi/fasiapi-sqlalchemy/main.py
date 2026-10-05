from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from src.utile.kafka import KafkaService
from src.utile.celery_conf import get_celery
from src.users import user_routes
from src.users import user_models
import database
from src.auth import auth_routes
from src.streamingapp import s_routes
from src.datascience import ds_routes
from src.fileupload import fs_routes

# Create database tables - usually at app startup (better to use migrations!)
# user_models.Base.metadata.create_all(bind=database.engine)
# 
@asynccontextmanager
async def kafkalifespan(app: FastAPI):
    
    app.state.kafka = KafkaService('localhost:29092','localhost:39092','localhost:49092')
    try:
        yield
    finally:
        app.state.kafka.close()



app = FastAPI(debug=True,lifespan=get_celery)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(user_routes.user_router)
app.include_router(auth_routes.auth)
app.include_router(s_routes.stram_rt)
app.include_router(ds_routes.ds_router)
app.include_router(fs_routes.fs_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}



# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}