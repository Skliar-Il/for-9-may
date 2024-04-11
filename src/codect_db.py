import boto3.s3
import boto3.session
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import async_session, AsyncSession, create_async_engine
import boto3

from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET
from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


metadata=MetaData()


session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, aws_session_token=None, region_name=None)
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)



    
# # Создать новый бакет
# s3.create_bucket(Bucket='bucket-name')

# # Загрузить объекты в бакет

# ## Из строки
s3.put_object(Bucket='for9may', Key='Test', Body=("егор лох"))

# ## Из файла
# s3.upload_file('this_script.py', 'bucket-name', 'py_script.py')
# s3.upload_file('this_script.py', 'bucket-name', 'script/py_script.py')

# Получить список объектов в бакете
# for key in s3.list_objects(Bucket='for9may'):
#     print(key)

# # Удалить несколько объектов
# forDeletion = [{'Key':'object_name'}, {'Key':'script/py_script.py'}]
# response = s3.delete_objects(Bucket='bucket-name', Delete={'Objects': forDeletion})

# # Получить объект
# get_object_response = s3.get_object(Bucket='zbucket-name',Key='py_script.py')
# print(get_object_response['Body'].read())
# s3 = boto3.resource('s3')
