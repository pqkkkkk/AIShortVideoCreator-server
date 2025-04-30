import uvicorn
from fastapi import FastAPI
from image import image_api
from user import user_api
from db import init_db

async def init_db_connection(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=init_db_connection)

app.include_router(image_api, prefix="/api/v1", tags=["image"])
app.include_router(user_api, prefix="/api/v1", tags=["user"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, port=8000)