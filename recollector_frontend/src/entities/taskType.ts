export type TaskStatus = 'processing' | 'completed' | 'failed';

export interface Task {
  task_id: string;
  status: TaskStatus;
  progress: number;
  current_step?: string;
  model_url?: string;
  viewer_url?: string;
  error?: string;
  vertices?: number;
  faces?: number;
  generation_time?: number;
}

export interface TaskStatusResponse {
  status: TaskStatus;
  progress: number;
  current_step?: string;
  model_url?: string;
  viewer_url?: string;
  error?: string;
  vertices?: number;
  faces?: number;
  generation_time?: number;
}