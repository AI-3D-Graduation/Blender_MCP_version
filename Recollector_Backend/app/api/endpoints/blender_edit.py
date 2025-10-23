"""
Blender 편집 관련 API 엔드포인트
"""
from fastapi import APIRouter, HTTPException, Path, Body
from pydantic import BaseModel
from typing import Optional
from app.services.blender_mcp_service import blender_service
from app.core.config import settings
import os

router = APIRouter()


class ChatEditRequest(BaseModel):
    message: str
    

class ChatEditResponse(BaseModel):
    success: bool
    message: str
    tools_used: list
    model_url: Optional[str] = None


@router.post(
    "/tasks/{task_id}/edit",
    summary="채팅으로 3D 모델 편집",
    description="자연어 채팅으로 Blender를 통해 3D 모델을 편집합니다.",
    response_model=ChatEditResponse
)
async def edit_model_with_chat(
    task_id: str = Path(..., description="편집할 모델의 작업 ID"),
    request: ChatEditRequest = Body(..., description="편집 요청 메시지")
):
    """
    사용자의 채팅 메시지로 3D 모델 편집
    
    예시:
    - "모델을 더 부드럽게 만들어줘"
    - "색상을 파란색으로 바꿔줘"
    - "모델 크기를 2배로 키워줘"
    - "조명을 더 밝게 해줘"
    """
    # 원본 모델 파일 경로
    model_path = os.path.join(settings.OUTPUT_DIR, f"{task_id}.glb")
    
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="모델 파일을 찾을 수 없습니다.")
    
    try:
        print(f"[DEBUG] 편집 시작 - Task ID: {task_id}, Message: {request.message}")
        
        # Blender MCP를 통해 모델 로드 (처음 편집 시에만)
        if not blender_service.is_model_loaded(task_id):
            print(f"[DEBUG] 첫 편집 - 모델 로드 시작: {model_path}")
            load_result = await blender_service.load_model(model_path, task_id)
            print(f"[DEBUG] 모델 로드 결과: {load_result}")
            
            if not load_result.get("success"):
                raise HTTPException(
                    status_code=500, 
                    detail=f"모델 로드 실패: {load_result.get('error')}"
                )
        else:
            print(f"[DEBUG] 이어서 편집 - 모델 로드 스킵")
        
        # 채팅 기반 편집 실행
        print(f"[DEBUG] 채팅 편집 시작")
        edit_result = await blender_service.chat_edit(
            user_message=request.message,
            model_path=model_path,
            task_id=task_id
        )
        print(f"[DEBUG] 편집 결과: {edit_result}")
        
        if not edit_result.get("success"):
            error_detail = edit_result.get("error", "편집 실패")
            print(f"[ERROR] 편집 실패: {error_detail}")
            raise HTTPException(status_code=500, detail=error_detail)
        
        # 편집된 모델 저장 (새 파일명으로)
        edited_model_path = os.path.join(settings.OUTPUT_DIR, f"{task_id}_edited.glb")
        print(f"[DEBUG] 모델 저장 시작: {edited_model_path}")
        save_result = await blender_service.save_model(edited_model_path)
        print(f"[DEBUG] 모델 저장 결과: {save_result}")
        
        if not save_result.get("success"):
            # 저장 실패해도 편집은 성공했으므로 경고만 추가
            edit_result["message"] += "\n(참고: 파일 저장에 실패했습니다)"
        
        return ChatEditResponse(
            success=True,
            message=edit_result.get("message", "편집이 완료되었습니다."),
            tools_used=edit_result.get("tools_used", []),
            model_url=f"/static/models/{task_id}_edited.glb" if save_result.get("success") else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"[ERROR] 예외 발생: {str(e)}")
        print(f"[ERROR] Traceback:\n{error_traceback}")
        raise HTTPException(status_code=500, detail=f"편집 중 오류 발생: {str(e)}")


@router.post(
    "/tasks/{task_id}/reset-edit",
    summary="편집 대화 초기화",
    description="현재 작업의 편집 대화 히스토리를 초기화합니다."
)
async def reset_edit_conversation(
    task_id: str = Path(..., description="초기화할 작업 ID")
):
    """편집 대화 히스토리 초기화"""
    blender_service.reset_conversation(task_id)
    return {"message": "대화 히스토리가 초기화되었습니다.", "task_id": task_id}


@router.get(
    "/tasks/{task_id}/download-edited",
    summary="편집된 모델 다운로드",
    description="편집된 3D 모델 파일을 다운로드합니다."
)
async def download_edited_model(
    task_id: str = Path(..., description="다운로드할 작업 ID")
):
    """편집된 GLB 모델 다운로드"""
    from fastapi.responses import FileResponse
    
    edited_path = os.path.join(settings.OUTPUT_DIR, f"{task_id}_edited.glb")
    
    if not os.path.exists(edited_path):
        raise HTTPException(status_code=404, detail="편집된 모델을 찾을 수 없습니다.")
    
    return FileResponse(
        path=edited_path,
        media_type="model/gltf-binary",
        filename=f"{task_id}_edited.glb"
    )
