import { useState, useRef, useEffect } from "react";
import { taskApi } from "../../entities";
import { TaskStatusResponse } from "../../entities/taskType";



export interface UseTaskPollingOptions {
  taskId: string | undefined;
  interval?: number;
  onCompleted?: (data: TaskStatusResponse) => void;
  onFailed?: (error: string) => void;
}

export interface UseTaskPollingReturn {
  taskStatus: TaskStatusResponse | null;
  progress: number;
  isLoading: boolean;
  error: string | null;
}

export const useTaskPolling = ({
  taskId,
  interval = 10000,
  onCompleted,
  onFailed
}: UseTaskPollingOptions): UseTaskPollingReturn => {
  const [taskStatus, setTaskStatus] = useState<TaskStatusResponse | null>(null);
  const [progress, setProgress] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const isPollingRef = useRef(false);
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const fetchTaskStatus = async () => {
    if (!taskId || isPollingRef.current) return;

    isPollingRef.current = true;

    try {
      const data = await taskApi.getStatus(taskId);
      setTaskStatus(data);
      setProgress(data.progress || 0);
      setIsLoading(false);

      if (data.status === 'completed') {
        stopPolling();
        onCompleted?.(data);
      } else if (data.status === 'failed') {
        stopPolling();
        setError(data.error || 'Task failed');
        onFailed?.(data.error || 'Unknown error');
      }
    } catch (err) {
      console.error('Error fetching task status:', err);
      setError('Failed to fetch task status');
      setIsLoading(false);
    } finally {
      isPollingRef.current = false;
    }
  };

  const stopPolling = () => {
    if (pollingIntervalRef.current) {
      clearInterval(pollingIntervalRef.current);
      pollingIntervalRef.current = null;
    }
  };

  useEffect(() => {
    if (!taskId) return;

    // 초기 로드
    fetchTaskStatus();

    // 폴링 시작
    pollingIntervalRef.current = setInterval(() => {
      fetchTaskStatus();
    }, interval);

    // 클린업
    return () => {
      stopPolling();
    };
  }, [taskId, interval]);

  return {
    taskStatus,
    progress,
    isLoading,
    error
  };
};