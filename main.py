from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
import subprocess
import uuid
from pydantic import BaseModel

app = FastAPI()

# 정적 파일 디렉토리를 앱에 마운트
app.mount("/static", StaticFiles(directory="static"), name="static")

# 요청 본문을 위한 Pydantic 모델
class AudioRequest(BaseModel):
    youtube_url: str

@app.post("/extract-audio/")
async def extract_audio(request_data: AudioRequest):  # Pydantic 모델을 사용
    # 고유한 파일 이름 생성, 정적 파일 디렉토리에 저장
    filename = f"static/{uuid.uuid4()}.wav"
    
    # yt-dlp를 사용하여 오디오 추출 및 WAV 형식으로 변환
    command = [
        "yt-dlp",
        "-x",  # 오디오만 추출
        "--audio-format", "wav",  # 오디오 포맷을 WAV로 설정
        "-o", filename,  # 출력 파일 이름 설정
        request_data.youtube_url  # YouTube 동영상 URL
    ]

    try:
        subprocess.run(command, check=True)
        # 파일 URL 반환
        return {"message": "Audio extracted successfully", "url": f"/static/{filename}"}
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="Failed to extract audio")
