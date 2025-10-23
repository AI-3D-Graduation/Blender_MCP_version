import time
import os
import json
import redis
import base64
import requests
from app.core.config import settings
from .email_service import send_result_email

MESHY_API_BASE_URL = settings.MESHY_API_BASE_URL
MESHY_API_KEY = settings.MESHY_API_KEY
OUTPUT_DIR = settings.OUTPUT_DIR
METADATA_DIR = settings.METADATA_DIR

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)


def _update_status(task_id, status_data):
    redis_client.set(task_id, json.dumps(status_data))


def _save_meta(task_id, meta_data):
    meta_path = os.path.join(METADATA_DIR, f"{task_id}.json")
    with open(meta_path, "w") as f:
        json.dump(meta_data, f, indent=4)


def run_ai_pipeline(task_id: str, image_path: str, original_filename: str, options: dict):
    print(f"[{task_id}] AI 파이프라인 시작. 옵션: {options}")

    headers = {"Authorization": f"Bearer {MESHY_API_KEY}"}

    try:
        _update_status(task_id, {"status": "processing", "progress": 10, "detail": "이미지 인코딩 및 AI 서버 요청 중..."})
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        img_b64 = base64.b64encode(image_bytes).decode("utf-8")
        image_data_url = f"data:image/png;base64,{img_b64}"

        payload = {"image_url": image_data_url, **options}
        response = requests.post(f"{MESHY_API_BASE_URL}/image-to-3d", headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        external_task_id = response.json().get("result")
        if not external_task_id:
            raise RuntimeError("외부 API에서 task_id를 받지 못했습니다.")

        _save_meta(task_id,
                   {"original_filename": original_filename, "options": options, "external_task_id": external_task_id})
        print(f"[{task_id}] 외부 AI 작업 생성 성공. 외부 Task ID: {external_task_id}")

        while True:
            status_response = requests.get(f"{MESHY_API_BASE_URL}/image-to-3d/{external_task_id}", headers=headers)
            status_response.raise_for_status()
            data = status_response.json()

            external_status = data.get("status")
            real_progress = data.get("progress", 0)

            current_data = json.loads(redis_client.get(task_id) or '{}')

            current_data['status'] = 'processing'
            current_data['progress'] = real_progress
            current_data['detail'] = f"3D 모델 생성 중... ({real_progress}%)"

            _update_status(task_id, current_data)
            print(f"[{task_id}] 외부 작업 상태: {external_status}, 진행률: {real_progress}%")

            if external_status == "SUCCEEDED":
                model_data = data.get("model_urls", {})
                glb_url = model_data.get("glb")

                if not glb_url:
                    raise RuntimeError("완료되었으나 모델 URL을 찾을 수 없습니다.")

                model_response = requests.get(glb_url)
                model_response.raise_for_status()

                output_filename = f"{task_id}.glb"
                output_path = os.path.join(OUTPUT_DIR, output_filename)
                with open(output_path, "wb") as f:
                    f.write(model_response.content)

                print(f"[{task_id}] 최종 모델 파일 다운로드 및 저장 완료.")

                current_data = json.loads(redis_client.get(task_id) or '{}')

                viewer_url = f"http://127.0.0.1:3000/result/{task_id}"
                completion_data = {
                    "status": "completed",
                    "progress": 100,
                    "viewer_url": viewer_url,
                    "model_url": f"/static/models/{output_filename}"
                }

                current_data.update(completion_data)
                recipient_email = current_data.get('recipient_email')
                if recipient_email:
                    import asyncio
                    email_sent, email_detail = asyncio.run(send_result_email(recipient_email, viewer_url))

                    current_data["email_status"] = {
                        "sent": email_sent,
                        "recipient": recipient_email,
                        "detail": email_detail
                    }

                _update_status(task_id, current_data)

                break

            elif external_status == "FAILED":
                error_message = data.get("error", {}).get("message", "알 수 없는 외부 API 에러")
                raise RuntimeError(error_message)

            time.sleep(10)

    except requests.exceptions.RequestException as e:
        error_detail = f"외부 API 호출 실패: {e.response.text if e.response else str(e)}"
        _update_status(task_id, {"status": "failed", "error": error_detail})
    except Exception as e:
        _update_status(task_id, {"status": "failed", "error": str(e)})
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)