import { apiClient } from "../../shared/api";


export interface EmailSubmitRequest {
  email: string;
}

export interface EmailSubmitResponse {
  message: string;
  task_id: string;
  email: string;
}

export const emailApi = {
  /**
   * Task에 이메일 등록
   */
  async submitEmail(taskId: string, email: string): Promise<EmailSubmitResponse> {
    const { data } = await apiClient.post<EmailSubmitResponse>(
      `/api/tasks/${taskId}/set-email`,
      { recipient_email: email }  // 백엔드 스키마와 일치시킴
    );
    return data;
  }
};