from boto3 import s3, session
import boto3
from boto3.s3.transfer import TransferConfig

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import async_session, AsyncSession, create_async_engine

from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker




session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, aws_session_token=None, region_name=None)
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)
config = TransferConfig(use_threads=False)



DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
metadata=MetaData()

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session




 
# # Создать новый бакет
# s3.create_bucket(Bucket='bucket-name')

# # Загрузить объекты в бакет

# ## Из строки
# s3.put_object(Bucket='for9may', Key='Test', Body=("егор лох"))

# ## Из файла
# s3.upload_file('utka.jpg', 'for9may', 'utka.jpg')
# s3.upload_file('this_script.py', 'bucket-name', 'script/py_script.py')

# Получить список объектов в бакете
# for key in s3.list_objects(Bucket='for9may'):
#     print(key)

# # Удалить несколько объектов
# forDeletion = [{'Key':'object_name'}, {'Key':'script/py_script.py'}]
# response = s3.delete_objects(Bucket='bucket-name', Delete={'Objects': forDeletion})

# # Получить объект
# get_object_response = s3.get_object(Bucket='for9may',Key='object_name')
# print(get_object_response['Body'])
# s3 = boto3.resource('s3')


# s3.download_file('for9may', 'utka.jpg', 'utka.jpg', Config=config)

