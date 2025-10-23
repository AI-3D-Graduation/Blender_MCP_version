interface ProgressBarProps {
  progress: number;
  className?: string;
}

export const ProgressBar = ({ progress, className = '' }: ProgressBarProps) => {
  return (
    <div
      className={`relative w-full max-w-md mx-auto flex flex-col items-center justify-center text-center ${className}`}
    >
      <div className="w-full bg-gray-700 rounded-full h-3 mb-4">
        <div
          className="bg-gradient-to-r from-purple-500 to-cyan-400 h-3 rounded-full transition-all duration-1000 ease-out"
          style={{ width: `${progress}%` }}
        />
      </div>
      <div className="text-white font-bold text-lg">
        {Math.round(progress)}%
      </div>
    </div>
  );
};
