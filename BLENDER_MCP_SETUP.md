# Blender MCP 통합 가이드

## 🎯 개요
이 프로젝트에 Blender MCP를 통합하여 AI 기반 채팅으로 3D 모델을 편집할 수 있습니다.

## 📋 사전 준비사항

### 1. Blender 설치
1. [Blender 공식 웹사이트](https://www.blender.org/download/)에서 최신 버전 다운로드
2. Windows에 설치 (기본 경로: `C:\Program Files\Blender Foundation\Blender 4.5`)
   지금 다운받으면 이 경로 그대로 되실겁니다
3. 설치 후 Blender가 정상 작동하는지 확인 (가운데에 큐브 보이면 끝)

### 2. Python 환경 설정
```bash
# Python 3.10 이상 필요
python --version
```

## 🚀 설치 단계

### Step 1: Blender MCP 서버 설치

```bash
# Blender MCP 서버 설치 (requirements.txt에도 추가해놓)
pip install blender-mcp

```

### Step 2: 백엔드 패키지 설치

```bash
cd Recollector_Backend

# 새로운 패키지 설치
pip install -r requirements.txt
```

### Step 3: 환경 변수 설정

`.env` 파일에 다음 내용 추가:

```env
# 기존 환경 변수들...

# Anthropic API Key (Claude 사용)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Anthropic API Key 발급:**
1. [Anthropic Console](https://console.anthropic.com/) 접속
2. API Keys 섹션에서 새 키 생성
3. 키를 복사하여 `.env` 파일에 추가

### Step 4: Blender MCP 서버 설정

Blender를 MCP 서버로 실행하도록 설정:

```bash
# Blender MCP 서버 초기화 (한 번만 실행)
python -m blender_mcp.server
```

## 🎮 사용 방법

### 1. 백엔드 시작

```bash
cd Recollector_Backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Blender MCP 서버 시작 (별도 터미널)

```bash
# MCP 서버 시작
venv\Scripts\python.exe -m blender_mcp.server
```


### 3. 프론트엔드 시작

```bash
cd recollector_frontend
npm start
```

### 4. 사용 예시

1. 이미지 업로드 및 3D 모델 생성
2. 결과 페이지에서 **"🎨 Edit with AI"** 버튼 클릭
3. 채팅창에서 자연어로 명령:
   - "모델을 더 부드럽게 만들어줘"
   - "색상을 파란색으로 바꿔줘"
   - "모델 크기를 2배로 키워줘"
   - "금속 재질로 바꿔줘"
   - "조명을 더 밝게 해줘"

## 🛠️ Blender MCP 기능

### 지원하는 편집 명령

1. **메쉬 편집**
   - 스무딩 (Smooth shading)
   - 리메싱 (Remesh)
   - 서브디비전 (Subdivision surface)
   - 크기 조정 (Scale)
   - 회전 (Rotate)

2. **재질 편집**
   - 색상 변경
   - 금속성 조정
   - 거칠기 조정
   - 투명도 조정

3. **조명 편집**
   - 조명 밝기 조정
   - 조명 색상 변경
   - 조명 위치 변경

4. **렌더링**
   - 썸네일 생성
   - 다양한 각도에서 렌더링

## 🔧 트러블슈팅

### 문제 1: Blender MCP 서버 연결 실패
```bash
# Blender 경로 확인
python -m blender_mcp config --show

# 서버 재시작
python -m blender_mcp serve --debug
```

### 문제 2: Anthropic API 키 오류
- `.env` 파일에 `ANTHROPIC_API_KEY`가 올바르게 설정되었는지 확인
- API 키가 활성화되어 있고 크레딧이 있는지 확인

### 문제 3: 모델 로드 실패
- GLB 파일이 올바른 경로에 있는지 확인
- Blender가 파일을 읽을 수 있는 권한이 있는지 확인

### 문제 4: 편집 명령이 작동하지 않음
- Blender MCP 서버가 실행 중인지 확인
- 백엔드 로그에서 오류 메시지 확인
- 더 구체적인 명령으로 다시 시도

## 📚 추가 리소스

- [Blender MCP 문서](https://github.com/your-repo/blender-mcp)
- [Anthropic Claude API 문서](https://docs.anthropic.com/)
- [Blender Python API](https://docs.blender.org/api/current/)

## 🎨 예시 명령어

```
사용자: "모델을 더 부드럽게 만들어줘"
→ Blender: Shade Smooth + Subdivision Surface 적용

사용자: "이 모델을 금색으로 만들어줘"
→ Blender: Metallic 재질 적용 + 골드 색상 설정

사용자: "모델 크기를 절반으로 줄여줘"
→ Blender: Scale 0.5 적용

사용자: "360도 회전하는 애니메이션 만들어줘"
→ Blender: 키프레임 애니메이션 생성 + 렌더링
```

## ⚙️ 고급 설정

### 커스텀 Blender 스크립트 추가
`Recollector_Backend/app/services/blender_scripts/` 폴더에 커스텀 Python 스크립트를 추가할 수 있습니다.

### MCP 도구 확장
새로운 Blender 기능을 MCP 도구로 추가하려면:
1. `blender_mcp_service.py` 수정
2. 새로운 도구 메서드 추가
3. Claude에게 도구 사용법 알림

## 💡 팁

1. **구체적으로 요청하기**: "색을 바꿔줘" 보다 "빨간색으로 바꿔줘"가 더 정확
2. **단계별 편집**: 한 번에 여러 편집을 요청하지 말고 하나씩 진행
3. **대화 초기화**: 잘못된 편집이 있으면 "대화 초기화" 버튼 클릭
4. **모델 다운로드**: 편집 후 새로운 모델을 다운로드할 수 있음

