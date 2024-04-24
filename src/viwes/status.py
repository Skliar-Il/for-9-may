from fastapi import status
from fastapi.responses import JSONResponse



async def json_status_response():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "success"})

async def json_status_db_response(details: list | dict):
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "success", "ditails": details})