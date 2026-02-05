from fastapi import FastAPI
from pydantic import BaseModel
import yt_dlp
import ffmpeg
import os
import uuid
#import openai  # Para subtítulos reales más adelante

app = FastAPI()

class VideoRequest(BaseModel):
    youtube_url: str

@app.post("/process")
def process_video(data: VideoRequest):
    # 1️⃣ Descargar vídeo
    video_id = str(uuid.uuid4())
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': f'/tmp/{video_id}.mp4'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([data.youtube_url])
    
    input_file = f'/tmp/{video_id}.mp4'
    output_file = f'/tmp/{video_id}_clip.mp4'

    # 2️⃣ Convertir a vertical y cortar 30s de ejemplo
    (
        ffmpeg
        .input(input_file, ss=0, t=30)
        .filter('scale', 720, 1280)
        .output(output_file)
        .run(overwrite_output=True)
    )

    # 3️⃣ Subtítulos de ejemplo
    subtitles = "Subtítulos generados automáticamente"

    return {
        "status": "ok",
        "clip": f"/tmp/{video_id}_clip.mp4",
        "subtitles": subtitles
    }
