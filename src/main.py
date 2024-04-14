from fastapi import FastAPI, UploadFile, File, Depends
from conect_db import s3
from typing import Annotated

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

@app.post("/new/person")
def new_persons(snl: str, date_birth: int, date_death: int, sity: str, history: str, main_photo: Annotated[ bytes, File() ], photo: Annotated[ list[bytes], File() ], medals: str, date_pulished: int, rank: str, role: bool):
    pass