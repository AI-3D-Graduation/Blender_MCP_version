import { apiClient } from "../../shared/api";


export interface ChatEditRequest {
  message: string;
}

export interface ChatEditResponse {
  success: boolean;
  message: string;
  tools_used: Array<{
    tool: string;
    arguments: any;
    result?: any;
    error?: string;
    success: boolean;
  }>;
  model_url?: string;
}

export const blenderApi = {
  /**
   * 채팅으로 3D 모델 편집
   */
  async editWithChat(taskId: string, message: string): Promise<ChatEditResponse> {
    const { data } = await apiClient.post<ChatEditResponse>(
      `/api/tasks/${taskId}/edit`,
      { message }
    );
    return data;
  },

  /**
   * 편집 대화 초기화
   */
  async resetConversation(taskId: string): Promise<void> {
    await apiClient.post(`/api/tasks/${taskId}/reset-edit`);
  },

  /**
   * 편집된 모델 다운로드
   */
  async downloadEdited(taskId: string): Promise<Blob> {
    const { data } = await apiClient.get(`/api/tasks/${taskId}/download-edited`, {
      responseType: 'blob',
    });
    return data;
  }
};
