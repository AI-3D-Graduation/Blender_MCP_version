
import { apiClient } from '../../shared/api';
import { TaskStatusResponse } from '../taskType';

export interface TaskDetailResponse extends TaskStatusResponse {
  viewer_url?: string;
  model_url?: string;
  vertices?: number;
  faces?: number;
  generation_time?: number;
}

export const taskApi = {
  /**
   * Task 상태 조회
   */
  async getStatus(taskId: string): Promise<TaskStatusResponse> {
    const { data } = await apiClient.get<TaskStatusResponse>(
      `/api/status/${taskId}`,
      {
        headers: {
          'Cache-Control': 'no-cache'
        }
      }
    );
    return data;
  },

  /**
   * Task 상세 정보 조회 (완료된 작업)
   */
  async getTask(taskId: string): Promise<TaskDetailResponse> {
    const { data } = await apiClient.get<TaskDetailResponse>(`/api/status/${taskId}`,
      {
        headers: {
          'Cache-Control': 'no-cache'
        }
      }
    );
    return data;
  }
};