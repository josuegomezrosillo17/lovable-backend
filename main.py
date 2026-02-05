from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class VideoRequest(BaseModel):
    youtube_url: str

@app.post("/process")
def process_video(data: VideoRequest):
    return {
        "status": "ok",
        "message": "Backend funcionando",
        "clips": []
    }
