from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import generation, blender_edit
import os

app = FastAPI(title="AI 3D Model Generator with Blender Integration")

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # 프론트엔드 URL
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

app.include_router(generation.router, prefix="/api", tags=["AI Model"])
app.include_router(blender_edit.router, prefix="/api", tags=["Blender Edit"])

static_dir = os.path.abspath("static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    return {"message": "AI 3D Model Generator API is running."}