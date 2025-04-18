from fastapi import FastAPI
from image import image_api

app = FastAPI()

app.include_router(image_api, prefix="/api/v1", tags=["image"])

@app.get("/")
async def root():
    return {"message": "Hello World"}