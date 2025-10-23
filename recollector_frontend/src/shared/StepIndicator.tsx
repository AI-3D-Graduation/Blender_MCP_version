import { FaCheck } from "react-icons/fa";

export type StepStatus = 'completed' | 'processing' | 'pending';

interface Step {
  id: number;
  label: string; // 한글 텍스트
  icon: string;
}

interface StepIndicatorProps {
  steps: Step[];
  currentStep: number;
  className?: string;
}

const getStepStatus = (stepId: number, currentStep: number): StepStatus => {
  if (stepId < currentStep) return 'completed';
  if (stepId === currentStep) return 'processing';
  return 'pending';
};

export const StepIndicator = ({ steps, currentStep, className = '' }: StepIndicatorProps) => {
  return (
    <div className={`space-y-6 ${className}`}>
      {steps.map((step, index) => {
        const status = getStepStatus(step.id, currentStep);
        return (
          <div
            key={step.id}
            className={`flex items-center justify-between max-w-md mx-auto p-4 rounded-lg transition-all duration-500 ${
              status === 'completed'
                ? 'bg-cyan-500/10 border border-cyan-500/30'
                : status === 'processing'
                ? 'bg-purple-500/10 border border-purple-500/30 animate-pulse'
                : 'bg-gray-800/50 border border-gray-600/30'
            }`}
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <div className="flex items-center space-x-3">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center transition-all duration-300 ${
                  status === 'completed'
                    ? 'bg-cyan-500 text-white'
                    : status === 'processing'
                    ? 'bg-purple-500 text-white'
                    : 'bg-gray-600 text-gray-400'
                }`}
              >
                {status === 'completed' ? (
                  <FaCheck />
                ) : status === 'processing' ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                ) : (
                  <i className={`${step.icon} text-lg`}></i>
                )}
              </div>
              <span
                className={`font-medium transition-colors duration-300 ${
                  status === 'completed'
                    ? 'text-cyan-400'
                    : status === 'processing'
                    ? 'text-purple-400'
                    : 'text-gray-500'
                }`}
              >
                {step.label}
              </span>
            </div>

            {status === 'processing' && (
              <div className="w-6 h-6 flex items-center justify-center">
                <div className="w-4 h-4 border-2 border-purple-400 border-t-transparent rounded-full animate-spin"></div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};
