from fastapi import *


app = FastAPI(
    title="For 9"
)

@app.get("/")
def title():
    return "For 9"

