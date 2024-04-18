from fastapi import FastAPI, UploadFile, File, Depends
from conect_db import s3
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from conect_db import get_async_session
from models.table import persons
from sqlalchemy import select, insert
from sqlalchemy import *
import json

from config import BUCKET


app = FastAPI(
    title="For 9"
)

@app.get("/")
def title():
    return "For 9"


@app.post("/test_db")
async def test(name: str, session: AsyncSession = Depends(get_async_session)):
    await session.execute(persons.insert().values({"SNL": name}))
    await session.commit()
    return 0


@app.post("/new/person")
async def new_persons(snl: str, date_birth: int, date_death: int, city: str, history: str, 
                      main_photo: Annotated[ bytes, File() ], photo: Annotated[ list[bytes], File() ], 
                      medals: list[str], date_pulished: int, rank: str, role: bool, contact_email: str, 
                      contact_SNL: str, contact_telegram: str,  
                      session: AsyncSession = Depends(get_async_session)):
    
    
    id = (await session.execute(select(persons.c.id))).all()[-1][0] + 1
    link_photo = []   
    s3.put_object(Bucket=BUCKET, Key=f"{id}_main.jpg", Body=main_photo) 
    for i in range(len(photo)):
        s3.put_object(Bucket = BUCKET, Key = f"{id}_{i}.jpg", Body = photo[i])
        link_photo.append(f"https://storage.yandexcloud.net/{BUCKET}/{id}_{i}.jpg")
     
        
    await session.execute(persons.insert().values({"SNL":snl, "date_birth":date_birth, "date_death":date_death, 
                                                   "city":city, "history":history, "main_photo":f"https://storage.yandexcloud.net/for9may/{id}_main.jpg", 
                                                   "photo":link_photo, "medals":medals, "date_pulished":date_pulished, 
                                                   "rank":rank, "role":role, "contact_email":contact_email, "contact_SNL":contact_SNL, "contact_telegram":contact_telegram}))
    await session.commit()
 
    #доделать базу данных и эндпоинты
    
    return 200