"""
Blender MCP Service
채팅 기반으로 Blender를 제어하여 3D 모델을 편집하는 서비스
"""
import json
import asyncio
import socket
from typing import Optional, Dict, Any
from anthropic import Anthropic
from app.core.config import settings

# Blender 소켓 서버 정보
BLENDER_HOST = 'localhost'
BLENDER_PORT = 9876


class BlenderMCPService:
    """Blender 소켓 서버와 통신하여 3D 모델을 편집하는 서비스"""
    
    def __init__(self):
        self.socket: Optional[socket.socket] = None
        self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.conversation_history = []
        self.request_id = 0
        self.loaded_models = {}  # task_id -> model_path 매핑
        
    async def connect(self):
        """Blender 소켓 서버에 연결"""
        if self.socket:
            print(f"[BlenderMCP] 이미 연결되어 있음")
            return
            
        try:
            print(f"[BlenderMCP] Blender 소켓 서버 연결 시작... ({BLENDER_HOST}:{BLENDER_PORT})")
            loop = asyncio.get_event_loop()
            
            # 소켓 생성 및 연결 (블로킹 작업을 executor에서 실행)
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # 10초 타임아웃
            
            await loop.run_in_executor(None, self.socket.connect, (BLENDER_HOST, BLENDER_PORT))
            print(f"[BlenderMCP] Blender 연결 완료!")
            
        except Exception as e:
            print(f"[BlenderMCP] 연결 실패: {str(e)}")
            import traceback
            traceback.print_exc()
            if self.socket:
                self.socket.close()
            self.socket = None
            raise Exception(f"Blender 소켓 서버에 연결할 수 없습니다. Blender가 실행 중이고 MCP 서버가 포트 {BLENDER_PORT}에서 대기 중인지 확인하세요.")
        
    async def disconnect(self):
        """Blender 소켓 서버 연결 해제"""
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
            finally:
                self.socket = None
    
    async def send_command(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Blender에 JSON-RPC 명령 전송"""
        if not self.socket:
            await self.connect()
        
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        
        try:
            # 명령 전송
            message = json.dumps(request) + "\n"
            print(f"[BlenderMCP] 전송: {message[:200]}")
            await asyncio.get_event_loop().run_in_executor(
                None, self.socket.sendall, message.encode('utf-8')
            )
            
            # 응답 수신 (타임아웃 증가)
            self.socket.settimeout(30)  # 30초 타임아웃
            response_data = await asyncio.get_event_loop().run_in_executor(
                None, self.socket.recv, 8192
            )
            
            if not response_data:
                raise Exception("Blender 서버로부터 응답이 없습니다")
            
            response_str = response_data.decode('utf-8').strip()
            print(f"[BlenderMCP] 수신: {response_str[:200]}")
            response = json.loads(response_str)
            return response
            
        except socket.timeout:
            print(f"[BlenderMCP] 타임아웃: Blender가 응답하지 않습니다")
            raise Exception("Blender 응답 타임아웃")
        except Exception as e:
            print(f"[BlenderMCP] 명령 전송/수신 오류: {str(e)}")
            raise e
            
    def is_model_loaded(self, task_id: str) -> bool:
        """모델이 이미 로드되었는지 확인"""
        return task_id in self.loaded_models
    
    async def load_model(self, model_path: str, task_id: str = None) -> Dict[str, Any]:
        """GLB 모델을 Blender에 로드"""
        print(f"[BlenderMCP] load_model 시작: {model_path}")
        
        try:
            if not self.socket:
                print(f"[BlenderMCP] 소켓이 없음, 연결 시도 중...")
                await self.connect()
                print(f"[BlenderMCP] 연결 완료")
            
            print(f"[BlenderMCP] load_model 명령 전송 중...")
            response = await self.send_command("load_model", {"file_path": model_path})
            print(f"[BlenderMCP] load_model 응답: {response}")
            
            if "error" in response:
                return {"success": False, "error": response["error"].get("message", "Unknown error")}
            
            # 로드 성공 시 기록
            if task_id:
                self.loaded_models[task_id] = model_path
                print(f"[BlenderMCP] 모델 로드 기록: task_id={task_id}")
            
            return {"success": True, "message": "Model loaded successfully", "data": response.get("result")}
            
        except Exception as e:
            print(f"[BlenderMCP] load_model 오류: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}
    
    async def chat_edit(self, user_message: str, model_path: str, task_id: str) -> Dict[str, Any]:
        """
        사용자의 채팅 메시지를 기반으로 모델 편집
        Claude가 Blender 명령을 생성하고 실행
        """
        try:
            print(f"[BlenderMCP] chat_edit 시작: {user_message}")
            
            if not self.socket:
                await self.connect()
            
            # 대화 히스토리에 사용자 메시지 추가
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            # Claude에게 Blender 명령 생성 요청
            system_prompt = """당신은 Blender 3D 모델 편집 전문가입니다.
사용자의 요청을 분석하여 Blender 편집 명령과 파라미터를 JSON 형식으로 생성하세요.

사용 가능한 명령:
1. change_color - 색상 변경
   예: {"command": "change_color", "params": {"r": 1.0, "g": 0.0, "b": 0.0}}

2. scale_model - 크기 변경
   예: {"command": "scale_model", "params": {"factor": 2.0}}

3. rotate_model - 회전
   예: {"command": "rotate_model", "params": {"axis": "Z", "angle": 45}}

4. apply_smooth - 스무딩 적용
   예: {"command": "apply_smooth", "params": {}}

5. add_object - 객체 추가 (Cube, Sphere, Cylinder, Cone 등)
   예: {"command": "add_object", "params": {"type": "CUBE", "position": [0, 0, -1], "scale": 1.0}}

6. change_material - 재질 변경
   예: {"command": "change_material", "params": {"metallic": 0.9, "roughness": 0.1}}

7. subdivide - 세분화 (더 부드럽게)
   예: {"command": "subdivide", "params": {"levels": 2}}

8. mirror - 미러 복제
   예: {"command": "mirror", "params": {"axis": "X"}}

9. array - 배열 복제
   예: {"command": "array", "params": {"count": 3, "offset": [2, 0, 0]}}

응답 형식:
{"command": "명령어", "params": {파라미터들}, "description": "무엇을 했는지 한글 설명"}

사용자의 요청을 정확히 파악하여 적절한 명령을 생성하세요."""
            
            # Claude API 호출
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                system=system_prompt,
                messages=self.conversation_history
            )
            
            # Claude의 응답 추출
            assistant_text = ""
            for block in response.content:
                if block.type == "text":
                    assistant_text += block.text
            
            print(f"[BlenderMCP] Claude 응답: {assistant_text}")
            
            # Claude 응답에서 JSON 명령 추출
            edit_params = self._extract_command_from_response(assistant_text, user_message)
            print(f"[BlenderMCP] 추출된 명령: {edit_params}")
            
            # Blender에 편집 명령 전송
            result = await self.send_command("execute_edit", edit_params)
            print(f"[BlenderMCP] 편집 결과: {result}")
            
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_text
            })
            
            return {
                "success": True,
                "message": edit_params.get("description", assistant_text) or "편집이 완료되었습니다.",
                "tools_used": [{"tool": "blender_edit", "command": edit_params.get("command"), "params": edit_params.get("params")}],
                "conversation_id": task_id
            }
            
        except Exception as e:
            print(f"[BlenderMCP] chat_edit 오류: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": f"채팅 편집 중 오류 발생: {str(e)}",
                "message": "편집에 실패했습니다. 다시 시도해주세요."
            }
    
    def _extract_command_from_response(self, claude_response: str, user_message: str) -> dict:
        """Claude의 응답에서 명령과 파라미터 추출"""
        import re
        import json
        
        # JSON 패턴 찾기
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        json_matches = re.findall(json_pattern, claude_response, re.DOTALL)
        
        for json_str in json_matches:
            try:
                data = json.loads(json_str)
                if "command" in data:
                    print(f"[BlenderMCP] JSON 명령 추출 성공: {data}")
                    return data
            except:
                continue
        
        # JSON 추출 실패 시 키워드 기반 명령 생성
        print(f"[BlenderMCP] JSON 추출 실패, 키워드 기반 명령 생성")
        user_lower = user_message.lower()
        
        # 색상 변경
        if any(word in user_lower for word in ["색상", "색깔", "color", "빨간", "파란", "초록", "노란"]):
            color = self._extract_color_from_response(claude_response, user_message)
            return {
                "command": "change_color",
                "params": color,
                "description": f"색상을 변경했습니다"
            }
        
        # 객체 추가
        elif any(word in user_lower for word in ["추가", "만들어", "생성", "add", "create"]):
            obj_type = "CUBE"
            if "구" in user_lower or "sphere" in user_lower:
                obj_type = "SPHERE"
            elif "원기둥" in user_lower or "실린더" in user_lower or "cylinder" in user_lower:
                obj_type = "CYLINDER"
            elif "원뿔" in user_lower or "cone" in user_lower:
                obj_type = "CONE"
            elif "정육면체" in user_lower or "큐브" in user_lower or "cube" in user_lower:
                obj_type = "CUBE"
            
            position = [0, 0, -1]  # 기본 위치 (모델 아래)
            if "위" in user_lower:
                position = [0, 0, 1]
            elif "옆" in user_lower or "오른쪽" in user_lower:
                position = [1, 0, 0]
            elif "왼쪽" in user_lower:
                position = [-1, 0, 0]
                
            return {
                "command": "add_object",
                "params": {"type": obj_type, "position": position, "scale": 1.0},
                "description": f"{obj_type}를 추가했습니다"
            }
        
        # 크기 변경
        elif any(word in user_lower for word in ["크기", "키워", "줄여", "scale", "크게", "작게"]):
            factor = 2.0
            if "2배" in user_lower or "두배" in user_lower:
                factor = 2.0
            elif "3배" in user_lower:
                factor = 3.0
            elif "절반" in user_lower or "반" in user_lower:
                factor = 0.5
            elif "작게" in user_lower or "줄여" in user_lower:
                factor = 0.5
            
            return {
                "command": "scale_model",
                "params": {"factor": factor},
                "description": f"크기를 {factor}배로 조정했습니다"
            }
        
        # 회전
        elif any(word in user_lower for word in ["회전", "돌려", "rotate"]):
            angle = 90
            axis = "Z"
            if "45" in user_lower:
                angle = 45
            elif "180" in user_lower:
                angle = 180
            
            return {
                "command": "rotate_model",
                "params": {"axis": axis, "angle": angle},
                "description": f"{axis}축으로 {angle}도 회전했습니다"
            }
        
        # 스무딩
        elif any(word in user_lower for word in ["부드럽", "smooth", "스무딩"]):
            return {
                "command": "apply_smooth",
                "params": {},
                "description": "스무딩을 적용했습니다"
            }
        
        # 세분화
        elif any(word in user_lower for word in ["세분화", "subdivide", "더 많은 면"]):
            return {
                "command": "subdivide",
                "params": {"levels": 2},
                "description": "모델을 세분화했습니다"
            }
        
        # 재질 변경
        elif any(word in user_lower for word in ["금속", "메탈", "metallic", "광택"]):
            return {
                "command": "change_material",
                "params": {"metallic": 0.9, "roughness": 0.1},
                "description": "금속 재질로 변경했습니다"
            }
        
        # 기본값
        return {
            "command": "generic_edit",
            "params": {"message": user_message},
            "description": "명령을 처리했습니다"
        }
        """Claude의 응답에서 RGB 색상 값 추출"""
        import re
        
        # change_color("색상명", R, G, B) 패턴 찾기
        pattern = r'change_color\([^,]+,\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)\)'
        match = re.search(pattern, claude_response)
        
        if match:
            r, g, b = match.groups()
            print(f"[BlenderMCP] RGB 추출 성공: R={r}, G={g}, B={b}")
            return {
                "r": float(r),
                "g": float(g),
                "b": float(b),
                "a": 1.0
            }
        
        # 매칭 실패 시 키워드로 색상 결정
        user_lower = user_message.lower()
        
        color_map = {
            "빨간": {"r": 1.0, "g": 0.0, "b": 0.0, "a": 1.0},
            "red": {"r": 1.0, "g": 0.0, "b": 0.0, "a": 1.0},
            "파란": {"r": 0.0, "g": 0.3, "b": 1.0, "a": 1.0},
            "blue": {"r": 0.0, "g": 0.3, "b": 1.0, "a": 1.0},
            "초록": {"r": 0.0, "g": 1.0, "b": 0.0, "a": 1.0},
            "green": {"r": 0.0, "g": 1.0, "b": 0.0, "a": 1.0},
            "노란": {"r": 1.0, "g": 1.0, "b": 0.0, "a": 1.0},
            "yellow": {"r": 1.0, "g": 1.0, "b": 0.0, "a": 1.0},
            "보라": {"r": 0.5, "g": 0.0, "b": 1.0, "a": 1.0},
            "purple": {"r": 0.5, "g": 0.0, "b": 1.0, "a": 1.0},
            "주황": {"r": 1.0, "g": 0.5, "b": 0.0, "a": 1.0},
            "orange": {"r": 1.0, "g": 0.5, "b": 0.0, "a": 1.0},
            "분홍": {"r": 1.0, "g": 0.4, "b": 0.7, "a": 1.0},
            "pink": {"r": 1.0, "g": 0.4, "b": 0.7, "a": 1.0},
            "흰": {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0},
            "white": {"r": 1.0, "g": 1.0, "b": 1.0, "a": 1.0},
            "검은": {"r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0},
            "black": {"r": 0.0, "g": 0.0, "b": 0.0, "a": 1.0},
        }
        
        for keyword, color in color_map.items():
            if keyword in user_lower:
                print(f"[BlenderMCP] 키워드 '{keyword}'로 색상 결정: {color}")
                return color
        
        # 기본값 (파란색)
        print(f"[BlenderMCP] 색상을 찾을 수 없어 기본값(파란색) 사용")
        return {"r": 0.0, "g": 0.3, "b": 1.0, "a": 1.0}
    
    async def save_model(self, output_path: str, format: str = "GLB") -> Dict[str, Any]:
        """편집된 모델을 파일로 저장"""
        if not self.socket:
            return {"success": False, "error": "Not connected to Blender"}
        
        try:
            print(f"[BlenderMCP] save_model 시작: {output_path}")
            response = await self.send_command("export_model", {
                "file_path": output_path,
                "format": format
            })
            print(f"[BlenderMCP] save_model 응답: {response}")
            
            if "error" in response:
                return {"success": False, "error": response["error"].get("message", "Unknown error")}
            
            return {"success": True, "path": output_path, "data": response.get("result")}
            
        except Exception as e:
            print(f"[BlenderMCP] save_model 오류: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def reset_conversation(self, task_id: str = None):
        """대화 히스토리 초기화"""
        self.conversation_history = []
        if task_id and task_id in self.loaded_models:
            # 모델 로드 기록도 제거 (다음에 다시 원본 로드)
            del self.loaded_models[task_id]
            print(f"[BlenderMCP] 모델 로드 기록 제거: task_id={task_id}")


# 싱글톤 인스턴스
blender_service = BlenderMCPService()
