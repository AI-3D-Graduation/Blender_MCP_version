# 깃허브 업로드 가이드

## 1. Git 초기화 (처음 한 번만)

```bash
# 프로젝트 루트 디렉토리로 이동
cd c:\Users\kimsu\Desktop\test

# Git 초기화
git init

# Git 사용자 설정 (전역 설정이 안 되어있다면)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## 2. .env 파일 보안 확인

**중요:** `.env` 파일이 `.gitignore`에 포함되어 있는지 확인하세요!

```bash
# .gitignore에 .env가 있는지 확인
cat Recollector_Backend\.gitignore | findstr ".env"
```

**결과가 나와야 합니다:**
```
.env
```

## 3. 민감한 정보 제거 확인

다음 파일들이 커밋되지 않도록 확인:
- ✅ `.env` (API 키 포함)
- ✅ `venv/` (가상환경)
- ✅ `node_modules/` (npm 패키지)
- ✅ `__pycache__/` (Python 캐시)
- ✅ `uploads/*` (업로드된 이미지)
- ✅ `static/models/*` (생성된 모델)
- ✅ `metadata/*` (메타데이터)

## 4. 파일 스테이징 및 커밋

```bash
# 모든 파일 추가
git add .

# 상태 확인 (민감한 파일이 포함되지 않았는지 확인)
git status

# 첫 커밋
git commit -m "Initial commit: Recollector - AI-Powered 3D Model Generator"
```

## 5. GitHub에 저장소 생성

1. https://github.com 접속
2. 로그인
3. 우측 상단 "+" → "New repository" 클릭
4. Repository 정보 입력:
   - **Repository name:** `recollector`
   - **Description:** `AI-Powered 3D Model Generator with Blender Integration`
   - **Visibility:** Public 또는 Private 선택
   - ⚠️ **Do NOT initialize with README** (이미 README.md가 있으므로)
5. "Create repository" 클릭

## 6. 원격 저장소 연결 및 푸시

GitHub에서 제공하는 명령어를 복사하거나 아래를 실행:

```bash
# 원격 저장소 추가 (YOUR_USERNAME을 실제 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/recollector.git

# 메인 브랜치 이름 설정
git branch -M main

# 푸시
git push -u origin main
```

## 7. 완료 확인

브라우저에서 `https://github.com/YOUR_USERNAME/recollector` 접속하여 확인!

## 📌 추가 작업 (선택사항)

### GitHub Topics 추가
Repository 페이지에서:
- Settings → Topics 추가
- 추천: `3d`, `ai`, `blender`, `fastapi`, `react`, `image-to-3d`, `claude-ai`

### README 개선
- 스크린샷/GIF 추가
- 데모 비디오 링크
- 라이브 데모 사이트 링크 (배포 시)

### GitHub Actions (CI/CD)
`.github/workflows/` 디렉토리에 자동화 설정 추가

## ⚠️ 주의사항

### 절대 커밋하면 안 되는 것들:
- ❌ `.env` 파일 (API 키 포함)
- ❌ `venv/` 디렉토리
- ❌ 생성된 모델 파일 (용량이 큼)
- ❌ 개인정보가 포함된 메타데이터

### 만약 실수로 커밋했다면:
```bash
# 특정 파일을 git history에서 제거
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch Recollector_Backend/.env" \
  --prune-empty --tag-name-filter cat -- --all

# 강제 푸시 (주의: 협업 중이면 팀원과 상의)
git push origin --force --all
```

## 🔄 일상적인 작업 플로우

```bash
# 변경사항 확인
git status

# 변경사항 스테이징
git add .

# 커밋
git commit -m "Add: 새로운 기능 추가"

# 푸시
git push
```

## 📦 태그 생성 (버전 관리)

```bash
# 버전 태그 생성
git tag -a v1.0.0 -m "Release version 1.0.0"

# 태그 푸시
git push origin v1.0.0
```

## 🌿 브랜치 전략 (선택사항)

```bash
# 새 기능 개발
git checkout -b feature/new-feature

# 작업 후 커밋
git add .
git commit -m "Feature: 새로운 편집 명령 추가"

# 메인 브랜치로 돌아가기
git checkout main

# 병합
git merge feature/new-feature

# 푸시
git push
```

## 📞 문제 해결

### 푸시 권한 오류
```bash
# GitHub 토큰 설정 필요
# Settings → Developer settings → Personal access tokens → Generate new token
# 토큰으로 로그인: https://YOUR_TOKEN@github.com/YOUR_USERNAME/recollector.git
```

### 대용량 파일 문제
```bash
# Git LFS 사용 (Large File Storage)
git lfs install
git lfs track "*.glb"
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

---

✅ **준비 완료!** 이제 `git push` 명령어를 실행하면 됩니다!
