// POST /api/generate 응답
export interface GenerateResponse {
  task_id: string;
  message: string;
}

// GET /api/status/{task_id} 응답
export interface GenerationStatus {
  task_id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number; // 0-100
  message?: string;
  result_url?: string; // 완료 시 3D 모델 URL
  error?: string; // 실패 시 에러 메시지
}

// API 에러 응답
export interface ApiErrorResponse {
  detail: string;
  error?: string;
}