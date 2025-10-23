import { apiClient } from '../shared/api/apiClient';
import { GenerateResponse, GenerationStatus } from './modelType';

/**
 * 이미지 파일을 업로드하고 3D 모델 생성 시작
 * @param file - 업로드할 이미지 파일
 * @returns task_id와 메시지
 */
export async function generateModel(file: File): Promise<GenerateResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await apiClient.post<GenerateResponse>('/api/generate', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
}

/**
 * 작업 ID로 생성 진행 상태 조회
 * @param taskId - 작업 ID
 * @returns 생성 상태와 진행률
 */
export async function getGenerationStatus(taskId: string): Promise<GenerationStatus> {
  const response = await apiClient.get<GenerationStatus>(`/api/status/${taskId}`);
  return response.data;
}

/**
 * 작업 삭제
 * @param taskId - 삭제할 작업 ID
 */
export async function deleteTask(taskId: string): Promise<void> {
  await apiClient.delete(`/api/tasks/${taskId}`);
}