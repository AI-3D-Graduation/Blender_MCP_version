# Recollector Frontend

React와 TypeScript 기반의 3D 모델링 생성 웹 어플리케이션입니다. 사용자가 사진을 업로드 하면 사진을 바탕으로 3D 모델을 생성할 수 있습니다.

## 📁 프로젝트 구조

```
src/
├─ app/
│  └─ router.tsx                 # 애플리케이션 라우팅 설정
│
├─ pages/                        # 페이지 컴포넌트
│  ├─ index.tsx                  
│  ├─ home.tsx                   
│  ├─ upload.tsx                 
│  ├─ loading.tsx                
│  ├─ result.tsx                 
│  └─ error.tsx                  
│
├─ component/                    # UI 컴포넌트
│  ├─ upload/                    # 업로드 관련 컴포넌트
│  │  ├─ PhotoUpload.tsx        
│  │  ├─ NoPhoto.tsx             
│  │  ├─ Preview.tsx             
│  │  ├─ Uploading.tsx           
│  │  └─ UploadTips.tsx          
│  │
│  ├─ loading/                   # 로딩 관련 컴포넌트
│  │  ├─ loadingProgress.tsx   
│  │  └─ emailForm.tsx           
│  │
│  └─ result/                    # 결과 관련 컴포넌트
│     └─ ModelViewer.jsx         # 3D 모델 뷰어 (Three.js)
│
├─ features/                     # 비즈니스 로직 및 커스텀 훅
│  ├─ index.ts                   
│  ├─ upload/                    # 업로드 기능
│  │  ├─ usePhotoUpload.ts      # 사진 업로드 로직
│  │  ├─ useDragAndDrop.ts      # 드래그 앤 드롭 기능
│  │  └─ useGenerateModel.ts    # 모델 생성 요청 로직
│  │
│  └─ loading/                   # 로딩 기능
│     ├─ useTaskPolling.ts      # 작업 상태 폴링
│     └─ useEmailSubmit.ts      # 이메일 제출 로직
│
├─ entities/                     # 데이터 모델 및 API
│  ├─ index.ts                   
│  ├─ api/                       # API 호출 함수
│  │  ├─ taskApi.ts             
│  │  ├─ modelApi.ts            
│  │  └─ emailApi.ts            
│  │
│  ├─ taskType.ts               
│  ├─ modelType.ts              
│  └─ modelGenerate.ts          # 모델 생성 관련 타입
│
├─ shared/                       # 공유 컴포넌트 및 유틸리티
│  ├─ index.ts                   
│  ├─ api/                       
│  │  ├─ index.ts               
│  │  ├─ apiClient.ts           # Axios 클라이언트 설정
│  │  └─ config.ts              # API 설정값
│  │
│  ├─ lib/                       # 유틸리티 함수
│  │  ├─ fileValidator.ts       
│  │  └─ pollingUtils.ts        
│  │
│  ├─ Button.tsx                 
│  ├─ Card.tsx                   
│  ├─ Navigation.tsx             
│  ├─ ProgressBar.tsx            
│  └─ StepIndicator.tsx          
│
└─ setupTests.js                # 테스트 설정
```


## 설치 및 실행

```bash
# 의존성 설치
npm install

# 개발 서버 실행 (포트 3000)
npm start

# 프로덕션 빌드
npm run build

# 테스트 실행
npm test
```

## 프록시 설정

백엔드 API는 `http://localhost:8000`으로 프록시 설정되어 있습니다.