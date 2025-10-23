(표준 MCP 프로토콜 전체를 그대로 따라 구현하지는 않았고, MCP와 최대한 유사하게 구현한겁니다.)

## ✨ 주요 기능

### 🖼️ Image to 3D
- 단일 이미지를 업로드하여 고품질 3D 모델(GLB) 생성
- Meshy AI API를 활용한 자동 3D 변환
- 실시간 진행률 표시 및 작업 상태 추적

### 🎨 AI 채팅 기반 3D 편집
- Claude AI와 Blender MCP 통합으로 자연어 명령 처리
- 실시간 모델 편집 및 미리보기
- 다양한 편집 명령 지원:
  - 색상 변경 ("빨간색으로 바꿔줘")
  - 객체 추가 ("위에 구를 추가해줘")
  - 크기/회전 조정 ("2배로 키워줘", "90도 회전시켜줘")
  - 재질 변경 ("금속 재질로 바꿔줘")
  - 스무딩/세분화 ("더 부드럽게 만들어줘")

### 🌐 인터랙티브 3D 뷰어
- Three.js 기반 실시간 3D 모델 렌더링
- 360도 회전, 확대/축소 지원
- 조명 밝기 조절
- GLB 포맷 모델 다운로드

### 📧 이메일 알림
- 모델 생성 완료 시 자동 이메일 발송
- 결과 페이지 직접 링크 제공

## 🏗️ 기술 스택

### Frontend
- **React** with TypeScript
- **Three.js** / React Three Fiber - 3D 렌더링
- **Tailwind CSS** - 스타일링
- **Axios** - API 통신
- **React Router** - 라우팅

### Backend
- **FastAPI** - REST API 서버
- **Python 3.10+**
- **Redis** - 작업 상태 관리
- **Meshy AI API** - Image to 3D 변환
- **Anthropic Claude API** - 자연어 처리
- **Blender MCP** - 3D 모델 편집

### Infrastructure
- **Blender 4.5+** - 3D 편집 엔진
- **WebSocket** - 실시간 통신
- **SMTP** - 이메일 발송

## 📋 사전 요구사항

### 필수 소프트웨어
- **Python 3.10 이상**
- **Node.js 16 이상**
- **Redis** (WSL 또는 Windows용)
- **Blender 4.5 이상**

### API 키
- **Meshy AI API Key** - [meshy.ai](https://meshy.ai)에서 발급
- **Anthropic API Key** - [console.anthropic.com](https://console.anthropic.com)에서 발급
- **Gmail App Password** - 이메일 알림용 (선택사항)

## 🚀 설치 및 실행

### 1. 저장소 클론

```bash
git clone https://github.com/yourusername/recollector.git
cd recollector
```

### 2. Redis 설치 및 실행

**WSL (권장):**
```bash
wsl redis-server --daemonize yes
```

Redis 확인:
```bash
wsl redis-cli ping
# 응답: PONG
```

### 3. 백엔드 설정

```bash
cd Recollector_Backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 API 키 입력
```

**.env 파일 설정:**
```env
# Meshy AI API
MESHY_API_KEY=your_meshy_api_key
MESHY_API_BASE_URL=https://api.meshy.ai/openapi/v1

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Email (선택사항)
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM=your_email@gmail.com
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_FROM_NAME=Recollector

# Anthropic API (Blender MCP용)
ANTHROPIC_API_KEY=your_anthropic_api_key
```

**백엔드 실행:**
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 4. Blender MCP 서버 설정

1. **Blender 실행**
2. **Scripting 탭**으로 이동
3. `Recollector_Backend/blender_mcp_addon.py` 파일 열기
4. **스크립트 실행** (▶ 버튼 또는 Alt+P)
5. 콘솔에서 확인:
   ```
   ✅ Blender listening on localhost:9876
   ```

### 5. 프론트엔드 설정

```bash
cd recollector_frontend

# 패키지 설치
npm install

# 개발 서버 실행
npm start
```

브라우저에서 `http://localhost:3000` 접속

## 📖 사용 방법

### 1단계: 이미지 업로드
- 메인 페이지에서 "Upload Picture" 클릭
- 이미지 파일 선택 또는 드래그 앤 드롭
- "Generate 3D Model" 버튼 클릭

### 2단계: 3D 모델 생성 대기
- 실시간 진행률 확인
- (선택) 이메일 주소 입력하여 완료 알림 받기
- 평균 처리 시간: 2-3분

### 3단계: 3D 모델 확인 및 다운로드
- 인터랙티브 3D 뷰어에서 모델 확인
- 마우스로 회전/확대/축소
- 밝기 조절 슬라이더 사용
- "Download Model" 버튼으로 GLB 파일 다운로드

### 4단계: AI로 모델 편집 (선택)
- "🎨 Edit with AI" 버튼 클릭
- 채팅창에 자연어 명령 입력:

**편집 예시:**
```
"색상을 빨간색으로 바꿔줘"
"모델 위에 구를 추가해줘"
"크기를 2배로 키워줘"
"금속 재질로 바꿔줘"
"모델을 더 부드럽게 만들어줘"
"90도 회전시켜줘"
```

- 편집된 모델은 자동 저장되고 뷰어에 표시
- "대화 초기화" 버튼으로 원본으로 복원

## 🎨 Blender 편집 명령어

| 카테고리 | 명령어 예시 | 설명 |
|---------|-----------|------|
| 색상 변경 | "빨간색으로 바꿔줘" | RGB 색상 적용 |
| 객체 추가 | "위에 정육면체 추가해줘" | 큐브, 구, 원기둥 등 추가 |
| 크기 조정 | "2배로 키워줘" | 모델 크기 변경 |
| 회전 | "90도 회전시켜줘" | X/Y/Z축 회전 |
| 재질 변경 | "금속 재질로 바꿔줘" | Metallic/Roughness 조정 |
| 스무딩 | "부드럽게 만들어줘" | Shade Smooth 적용 |
| 세분화 | "더 세밀하게 만들어줘" | Subdivision Surface |

## 🗂️ 프로젝트 구조

```
recollector/
├── Recollector_Backend/          # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py               # FastAPI 앱 진입점
│   │   ├── api/endpoints/        # API 라우트
│   │   │   ├── generation.py    # 3D 생성 API
│   │   │   └── blender_edit.py  # Blender 편집 API
│   │   ├── core/
│   │   │   └── config.py         # 환경 설정
│   │   ├── services/
│   │   │   ├── ai_pipeline.py   # Meshy AI 통합
│   │   │   ├── blender_mcp_service.py # Blender 통신
│   │   │   └── email_service.py # 이메일 발송
│   │   └── schemas/              # Pydantic 스키마
│   ├── blender_mcp_addon.py     # Blender 소켓 서버
│   ├── requirements.txt          # Python 의존성
│   ├── .env.example             # 환경 변수 예시
│   └── static/models/           # 생성된 GLB 파일
│
├── recollector_frontend/         # React 프론트엔드
│   ├── src/
│   │   ├── pages/               # 페이지 컴포넌트
│   │   ├── component/           # UI 컴포넌트
│   │   ├── entities/            # API 클라이언트
│   │   ├── features/            # 비즈니스 로직
│   │   └── shared/              # 공유 컴포넌트
│   ├── public/
│   └── package.json
│
├── BLENDER_MCP_SETUP.md         # Blender MCP 설정 가이드
└── README.md                     # 이 파일
```

## 🔧 트러블슈팅

### Redis 연결 오류
```
ConnectionRefusedError: [WinError 10061]
```
**해결방법:**
```bash
# Redis 서버 시작
wsl redis-server --daemonize yes

# 상태 확인
wsl redis-cli ping
```

### Blender MCP 타임아웃
**증상:** 편집 명령 전송 후 응답 없음

**해결방법:**
1. Blender가 실행 중인지 확인
2. `blender_mcp_addon.py` 스크립트가 실행 중인지 확인
3. Blender 콘솔에서 "✅ Blender listening on localhost:9876" 메시지 확인
4. 포트 9876이 사용 가능한지 확인

### 모델 생성 실패
**원인:** Meshy AI API 크레딧 부족 또는 API 키 오류

**해결방법:**
1. `.env` 파일의 `MESHY_API_KEY` 확인
2. [Meshy AI 대시보드](https://meshy.ai)에서 크레딧 확인
3. API 키 권한 확인

### 편집 이력 사라짐
**원인:** "대화 초기화" 버튼 클릭 또는 페이지 새로고침

**해결방법:**
- 편집은 연속으로 진행됩니다
- "대화 초기화"를 누르면 원본으로 되돌아갑니다
- 편집된 모델은 `{task_id}_edited.glb`로 저장됩니다
