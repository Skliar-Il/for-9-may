from fastapi import FastAPI, UploadFile, File, Depends, Query
from conect_db import s3
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from conect_db import get_async_session
from models.table import persons, admins
from models.table import token as table_token
from sqlalchemy import select, insert
import json, hashlib, random, string

from config import BUCKET




app = FastAPI(
    title="For 9"
)

@app.get("/")
def title():
    return "For 9 may"





@app.post("/api/v1/login")
async def login(email: str, password: str, session: AsyncSession = Depends(get_async_session)):
    
    password = hashlib.sha3_512(password.encode()).hexdigest()
    
    check = await session.execute(admins.select().where(admins.c.password == password))
    
    if check.all() == []:
        return 401, {"status":"error", "detail":"неверно введен логин или пароль"}
    
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = random.randint(8, 12)
    token = ''.join(random.choice(chars) for x in range(size))
    
    await session.execute(table_token.update().values({"token":token}).where(table_token.c.id == 1))
    await session.commit()
    return 200, {"status":"sacces", "data":token}    



@app.post("/api/v1/unreadedPersons")
async def new_persons(snl: str, date_birth: int, date_death: int, city: str, history: str, 
                    date_pulished: int, rank: str, role: bool, contact_email: str, 
                    contact_SNL: str, contact_telegram: str, medals: list[str | None] = None, main_photo: Annotated[ bytes | None, File() ] = None,
                    photo: Annotated[ list[bytes | None], File() ] = None, session: AsyncSession = Depends(get_async_session)):
    
    link_main_photo=""
    link_photo = []  
    id = (await session.execute(select(persons.c.id))).all()[-1][0] + 1 
    
    
    if main_photo:
        s3.put_object(Bucket=BUCKET, Key=f"{id}_main.jpg", Body=main_photo) 
        link_photo=f"https://storage.yandexcloud.net/for9may/{id}_main.jpg"
        
    if photo != [b'']:
        for i in range(len(photo)):
            s3.put_object(Bucket = BUCKET, Key = f"{id}_{i}.jpg", Body = photo[i])
            link_photo.append(f"https://storage.yandexcloud.net/{BUCKET}/{id}_{i}.jpg")
     
        
    await session.execute(persons.insert().values({"SNL":snl, "date_birth":date_birth, "date_death":date_death, 
                                                   "city":city, "history":history, "main_photo":link_main_photo, 
                                                   "photo":link_photo, "medals":medals, "date_pulished":date_pulished, 
                                                   "rank":rank, "role":role, "contact_email":contact_email, "contact_SNL":contact_SNL, "contact_telegram":contact_telegram}))
    await session.commit()
 
    #доделать базу данных и эндпоинты
    return 200, {"status":"success"}



@app.get("/api/v1/unreadedPersons")
async def get_persons(token_query: str, session: AsyncSession = Depends(get_async_session)):
    print(token_query)
    # if TOKEN != token_query:
    #     return 401, {"status":"error", "detail":"необходимо войти в аккаунт"}

    data = await session.execute(persons.select())
    print(data.mappings().all()[20])
    return 200, {"status":"sacces", "data":"data"}

#токен в базу данных отдельно выводить массивы иначе очень неочень выглядит
#токен добавлен надо его теперь просто выводить(при апуске проекта что то вписать в таблицу) передалать массивы и проверку токена 




@app.get("/new_password")
async def new_password(session: AsyncSession = Depends(get_async_session)):
    await session.execute(admins.insert().values({"login":"asd", "password":"9e61f1c8210c120fcd41343fd2eb8734fc953dee04ed31830da70173cdb3e561be7bb0138aacd5d277a3cfe6cb7194f1ceb7528b0327f48979d4990ad2acb4e5"}))
    await session.commit()
    return 0