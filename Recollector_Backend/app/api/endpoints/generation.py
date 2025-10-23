import uuid
import os
import json
import redis
from app.core.config import settings
from fastapi import APIRouter, File, UploadFile, BackgroundTasks, HTTPException, Depends, Path, Form, Body
from starlette.responses import JSONResponse
from app.services.ai_pipeline import run_ai_pipeline
from app.schemas.generation import AIOptions, SetEmailRequest


router = APIRouter()

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

UPLOAD_DIR = settings.UPLOAD_DIR
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/generate",
             summary="3D 모델 생성 시작",
             description="이미지 파일과 AI 옵션을 받아 3D 모델 생성을 비동기적으로 시작합니다.",
             status_code=202)
async def generate_3d_model(
    background_tasks: BackgroundTasks,
    options: AIOptions = Depends(),
    file: UploadFile = File(..., description="3D 모델을 생성할 원본 이미지 파일 (JPG, PNG 등)"),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드할 수 있습니다.")

    task_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{task_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    initial_status = {"status": "processing", "progress": 0}
    redis_client.set(task_id, json.dumps(initial_status))

    background_tasks.add_task(
        run_ai_pipeline,
        task_id=task_id,
        image_path=file_path,
        original_filename=file.filename,
        options=options.dict(),
    )

    return JSONResponse(
        status_code=202,
        content={"task_id": task_id, "status_url": f"/api/status/{task_id}"}
    )


@router.get("/status/{task_id}",
            summary="작업 상태 조회",
            description="제공된 Task ID에 해당하는 작업의 현재 상태와 진행률을 조회합니다."
            )
async def get_task_status(task_id: str = Path(..., description="조회할 작업의 고유 ID", example="a1b2c3d4-e5f6-7890-1234-567890abcdef")):
    status_json = redis_client.get(task_id)

    if not status_json:
        raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다.")

    return json.loads(status_json)


@router.delete("/tasks/{task_id}",
               summary="작업 및 파일 삭제",
               description="완료되거나 실패한 작업을 시스템에서 완전히 삭제합니다."
               )
async def delete_task(task_id: str = Path(..., description="삭제할 작업의 고유 ID", example="a1b2c3d4-e5f6-7890-1234-567890abcdef")):
    if not redis_client.exists(task_id):
        raise HTTPException(status_code=404, detail=f"Task ID '{task_id}' not found.")

    print(f"Deleting task and files for ID: {task_id}")

    model_path = settings.OUTPUT_DIR / f"{task_id}.glb"
    meta_path = settings.METADATA_DIR / f"{task_id}.json"

    deleted_files = []
    errors = []

    try:
        if os.path.exists(model_path):
            os.remove(model_path)
            deleted_files.append(str(model_path))
    except Exception as e:
        errors.append(f"Failed to delete model file: {e}")

    try:
        if os.path.exists(meta_path):
            os.remove(meta_path)
            deleted_files.append(str(meta_path))
    except Exception as e:
        errors.append(f"Failed to delete metadata file: {e}")

    redis_client.delete(task_id)

    if errors:
        raise HTTPException(status_code=500, detail={"message": f"Task '{task_id}' removed from Redis, but file deletion failed.", "errors": errors})

    return {
        "message": f"Task '{task_id}' and associated files deleted successfully.",
        "deleted_files": deleted_files
    }


@router.post(
    "/tasks/{task_id}/set-email",
    summary="작업에 결과 통보 이메일 설정",
    description="진행 중이거나 완료된 작업에 대해 결과 통보를 받을 이메일 주소를 설정합니다."
)
async def set_email_for_task(
        task_id: str = Path(..., description="이메일 주소를 설정할 작업의 고유 ID"),
        request_body: SetEmailRequest = Body(...)
):
    status_json = redis_client.get(task_id)
    if not status_json:
        raise HTTPException(status_code=404, detail=f"Task ID '{task_id}' not found.")

    status_data = json.loads(status_json)
    status_data['recipient_email'] = request_body.recipient_email
    redis_client.set(task_id, json.dumps(status_data))

    return {"message": "Email address has been set for the task.", "task_id": task_id,
            "recipient_email": request_body.recipient_email}