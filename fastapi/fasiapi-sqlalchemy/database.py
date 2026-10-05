from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker
from contextlib import contextmanager


from urllib.parse import quote_plus

db_passwd = quote_plus("djangomypassword")

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://djangouser:{db_passwd}@172.21.0.3:5432/fastpialchemy"
SQLALCHEMY_DATABASE_URL_FASTAPI = f"postgresql+asyncpg://djangouser:{db_passwd}@172.21.0.3:5432/fastpialchemy"


engine = create_async_engine(SQLALCHEMY_DATABASE_URL_FASTAPI, pool_pre_ping=True,echo=True)
SessionLocal = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False,autocommit=False,autoflush=False)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
            await db.commit()
        except:
            await db.rollback()
            raise
        finally:
            await db.close()


# Raw Sql Database Connection
from psycopg2 import connect,pool
db_raw_passwd = quote_plus("datasciencepassword")
RAW_DATABASE_URL = f"postgresql://datascience:{db_raw_passwd}@172.21.0.3:5432/datasciencecsv"

db_pool = pool.ThreadedConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=RAW_DATABASE_URL
)



@contextmanager
def get_db_raw():

    conn_raw = db_pool.getconn()
    try:
        cursor = conn_raw.cursor()

        try:
            yield cursor
            conn_raw.commit()
        except Exception as e:
            conn_raw.rollback()
            raise
        finally:
            cursor.close()
    finally:
        db_pool.putconn(conn_raw)

