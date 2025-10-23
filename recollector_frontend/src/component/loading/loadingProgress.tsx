import { ProgressBar, StepIndicator } from "../../shared";
import { calculateCurrentStep, calculateEstimatedTime } from "../../shared/lib/pollingUtils";
import { EmailForm } from "./emailForm";


interface LoadingProgressProps {
  taskId: string | undefined;
  progress: number;
}

const STEPS = [
  { id: 0, label: '서버에 이미지 업로드', icon: 'ri-check-line' },
  { id: 1, label: '사진 내부 오브젝트 분석', icon: 'ri-search-eye-line' },
  { id: 2, label: '3D 모델링 파일로 변환', icon: 'ri-3d-view' },
  { id: 3, label: '.glb 파일 변환', icon: 'ri-check-double-line' }
];

export const LoadingProgress = ({ taskId, progress }: LoadingProgressProps) => {
  const currentStep = calculateCurrentStep(progress);
  const estimatedTime = calculateEstimatedTime(progress);

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header - Centered */}
      <div className="text-center space-y-4 mb-12 animate-fade-in">
        <h1 className="text-4xl font-bold">
          <span className="bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
            Converting photo into 3D model...
          </span>
        </h1>

        <p className="text-gray-200 text-lg">
          Your moment is transforming into realistic right now
        </p>

        <p className="text-gray-500 text-xs"> 변환에는 약 5분 정도 소요됩니다. </p>
      </div>

      {/* Two Column Layout - Equal Width */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left Container - Progress Bar + Email Form */}
        <div className="space-y-6">
          <ProgressBar progress={progress} className="animate-fade-in animation-delay-200" />
          
          <EmailForm taskId={taskId} />
        </div>

        {/* Right Container - Step Indicator */}
        <div className="flex items-start justify-center animate-fade-in animation-delay-600">
          <StepIndicator
            steps={STEPS}
            currentStep={currentStep}
          />
        </div>
      </div>
    </div>
  );
};