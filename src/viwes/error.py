from fastapi.responses import JSONResponse
from fastapi import status

async def json_error_auth_respons(details: str | dict):
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content = {"status":"error", "details":details})