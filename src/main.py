from fastapi import FastAPI, UploadFile, File, Depends
from conect_db import s3
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from conect_db import get_async_session
from models.table import persons
import sqlalchemy

from config import BUCKET

app = FastAPI(
    title="For 9"
)

@app.get("/")
def title():
    return "For 9"

# @app.post("/new/photo")
# async def photo(filename: str, file_body: Annotated[ bytes, File() ]):
#     s3.put_object(Bucket=BUCKET, Key=filename, Body=(file_body))
#     return 0




@app.post("/test_db")
async def test(name: str, session: AsyncSession = Depends(get_async_session)):
    await session.execute(persons.insert().values({"SNL": name}))
    await session.commit()
    return 0


@app.post("/new/person")
async def new_persons(snl: str, date_birth: int, date_death: int, city: str, history: str, main_photo: Annotated[ bytes, File() ], photo: Annotated[ list[bytes], File() ], medals: list, date_pulished: int, rank: str, role: bool, session: AsyncSession = Depends(get_async_session)):
    await session.execute(persons.insert().values({"SNL":snl, "date_birth":date_birth, "date_death":date_death, "city":city, "history":history, "main_photo":None, "photo":None, "medals":list, "date_pulished":date_pulished, "rank":rank, "role":role}))
    await session.commit()
    # id = session.lastrowid
    # id_photo = [str]
    
    # s3.put_object(bucket=BUCKET, Key=f"{id}_main.jpg", Body=main_photo)
    
    # for i in range(len(photo)):
    #     s3.put_object(bucket = BUCKET, Key = f"{id}_{i}.jpg", Body = main_photo[i])
    #     id_photo.append(f"https://storage.yandexcloud.net/{BUCKET}/{id}_{i}.jpg")
        
    return 0