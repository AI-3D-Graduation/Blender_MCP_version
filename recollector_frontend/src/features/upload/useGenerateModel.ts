import { useState } from 'react';
import { GenerateResponse } from '../../entities/modelType';
import { generateModel } from '../../entities/modelGenerate';

interface UseGenerateModelReturn {
  taskId: string | null;
  isGenerating: boolean;
  error: string | null;
  startGeneration: (file: File) => Promise<void>;
  reset: () => void;
}

export const useGenerateModel = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [taskId, setTaskId] = useState<string | null>(null);

  const startGeneration = async (file: File): Promise<string> => {
    setIsGenerating(true);
    setError(null);

    try {
      const response = await generateModel(file);
      
      // task_id 추출 (백엔드 응답에 따라 조정)
      const taskId = response.task_id;
      setTaskId(taskId);
      
      return taskId; // task_id 반환
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || err.message || 'Model generation failed';
      setError(errorMessage);
      throw err;
    } finally {
      setIsGenerating(false);
    }
  };

  return {
    startGeneration,
    isGenerating,
    error,
    taskId,
  };
};