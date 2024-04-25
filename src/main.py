from fastapi import FastAPI, UploadFile, File, Depends, Query, status
from fastapi.middleware.cors import CORSMiddleware
from conect_db import s3
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from conect_db import get_async_session
from models.table import persons, admins
from models.table import token as table_token
from sqlalchemy import select, insert
import json, hashlib, random, string
from viwes.status import json_status_response, json_status_db_response
from viwes.error import json_error_auth_respons

from config import BUCKET




app = FastAPI(
    title="For 9"
)

@app.get("/")
def title():
    return "For 9 may"

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






@app.post("/api/v1/login")
async def login(email: str, password: str, session: AsyncSession = Depends(get_async_session)):
    
    password = hashlib.sha3_512(password.encode()).hexdigest()
    
    check = await session.execute(admins.select().where(admins.c.password == password))
    
    if check.all() == []:
        return await json_error_auth_respons("неверно введен логин или пароль")
    
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = random.randint(8, 12)
    token = ''.join(random.choice(chars) for x in range(size))
    
    await session.execute(table_token.update().values({"token":token}).where(table_token.c.id == 0))
    await session.commit()
    return await json_status_db_response(token)    



@app.post("/api/v1/unreadedPersons")
async def new_persons(snl: str, date_birth: int, date_death: int, city: str, history: str, 
                    date_pulished: int, rank: str, role: bool, contact_email: str, 
                    contact_SNL: str, contact_telegram: str, medals: list[str | None] = None, main_photo: Annotated[ bytes | None, File() ] = None,
                    photo: Annotated[ list[bytes | None], File() ] = None, session: AsyncSession = Depends(get_async_session)):
    
    
    medals = medals[0].split(",")
    link_main_photo=""
    link_photo = ""  
    medals_all = ""
    id = (await session.execute(select(persons.c.id))).all()[-1][0] + 1 
    
    
    if main_photo:
        s3.put_object(Bucket=BUCKET, Key=f"{id}_main.jpg", Body=main_photo) 
        link_photo=f"https://storage.yandexcloud.net/for9may/{id}_main.jpg"
        
    if photo != [b'']:
        for i in range(len(photo)):
            s3.put_object(Bucket = BUCKET, Key = f"{id}_{i}.jpg", Body = photo[i])
            link_photo+=f"https://storage.yandexcloud.net/{BUCKET}/{id}_{i}.jpg_"
    
    if medals != []:        
        for i in range(len(medals)):
            medals_all+=f"{medals[i]}_"
            print(f"{medals[i]}_")
    
    
    await session.execute(persons.insert().values({"SNL":snl, "date_birth":date_birth, "date_death":date_death, 
                                                   "city":city, "history":history, "main_photo":link_main_photo, 
                                                   "photo":link_photo, "medals":medals_all[:-1], "date_pulished":date_pulished, 
                                                   "rank":rank, "role":role, "contact_email":contact_email, "contact_SNL":contact_SNL, "contact_telegram":contact_telegram}))
    await session.commit()
 
    #доделать базу данных и эндпоинты
    return await json_status_response()





@app.get("/api/v1/unreadedPersons")
async def get_persons(token_query: str, session: AsyncSession = Depends(get_async_session)):

    token_fin = (await session.execute(select(table_token.c.token))).all()[0][0]

    if token_query != token_fin:
        return await json_error_auth_respons("войдите в аккаунт")

    data = await session.execute(persons.select().where(persons.c.check == False))
    
    return {"status": "succes", "ditail": data.mappings().all()}

#токен в базу данных отдельно выводить массивы иначе очень неочень выглядит
#токен добавлен надо его теперь просто выводить(при апуске проекта что то вписать в таблицу) передалать массивы и проверку токена 





@app.delete("/api/v1/unreadedPersons/{id}")
async def delet_person(id: int, session: AsyncSession = Depends(get_async_session)):
    await session.execute(persons.delete().where(persons.c.id == id))
    await session.commit()
    return await json_status_response()





@app.post("/api/v1/persons")
async def ckeck_persons(id: int, token_query: str, city: str, date_birth: int, 
                        date_death: int, history: str, role: bool, main_photo: str, SNL: str, 
                        date_pulished: int, rank: str, photo: list[str], 
                        medals: list[str], 
                        session: AsyncSession = Depends(get_async_session)):
    
    token_fin = (await session.execute(select(table_token.c.token))).all()[0][0]
    medals_srt = ""
    photo_str = ""
    
    if token_query != token_fin:
        return await json_error_auth_respons("войдите в аккаунт")
    
    for i in range(len(medals)):
        medals_srt += f"{medals[i]}_"
    for i in range(len(photo)):
        photo_str += f"{photo[i]}_"
    
    
    
    
    await session.execute(persons.update().values({"check": True, "city": city, "date_birth": date_birth, 
                                                   "date_death": date_death, "history": history, "role": role,
                                                   "main_photo": main_photo, "medals": medals_srt, "SNL": SNL,
                                                   "photo": photo_str, "date_pulished": date_pulished, "rank": rank}).where(persons.c.id == id))
    await session.commit()
    
    return await json_status_response()





@app.get("/api/v1/persons")
async def get_check_persons(session: AsyncSession = Depends(get_async_session)):
    data = await session.execute(select(persons.c.id, persons.c.city, persons.c.date_birth, 
                                        persons.c.date_death, persons.c.history, 
                                        persons.c.role, persons.c.main_photo, persons.c.SNL, 
                                        persons.c.date_pulished).where(persons.c.check == True))
    
    return {"status": "succes", "ditails": data.mappings().all()}

@app.post("/start")
async def start(password_start: str, session: AsyncSession = Depends(get_async_session)):
    if password_start != "jopabobra45":
        return {"status": "error"}
    
    await session.execute(persons.insert().values({"SNL":"egor", "history": "test"}))
    await session.commit()
    
    await session.execute(table_token.insert().values({"token": "", "id": 0}))
    await session.commit()
    
    await session.execute(admins.insert().values({"login": "asd", "password": "180b8babdf49cadca266e4af0ccfe711bc83bf014e4a511913996e05ee447d144d8bf70ec12a5ea2edf1b909be3a31e0c89a91980d450897092dc2acf5702c25"}))
    await session.commit()