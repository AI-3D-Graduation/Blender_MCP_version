import { apiClient } from "../../shared/api";


export interface GenerateModelRequest {
  image: File;
}

export interface GenerateModelResponse {
  task_id: string;
  status: string;
  message?: string;
}

export const modelApi = {
  /**
   * 이미지 업로드 및 3D 모델 생성 시작
   */
  async generate(file: File): Promise<GenerateModelResponse> {
    const formData = new FormData();
    formData.append('file', file);  // 백엔드 파라미터명과 일치시킴

    const { data } = await apiClient.post<GenerateModelResponse>(
      '/api/generate',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return data;
  },

  /**
   * 생성된 모델 다운로드
   */
  async download(taskId: string): Promise<Blob> {
    const { data } = await apiClient.get(`/api/task/${taskId}/download`, {
      responseType: 'blob',
    });
    return data;
  }
};