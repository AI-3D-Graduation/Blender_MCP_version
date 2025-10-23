import { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { LoadingProgress } from "../component/loading/loadingProgress";
import { useTaskPolling } from "../features";
import { Navigation } from "../shared";

export default function Loading() {
  const navigate = useNavigate();
  const { taskId } = useParams<{ taskId: string }>();

  const { progress, error } = useTaskPolling({
    taskId,
    interval: 10000,
    onCompleted: () => {
      setTimeout(() => {
        navigate(`/result/${taskId}`, { replace: true });
      }, 1000);
    },
    onFailed: (errorMsg) => {
      alert(`Generation failed: ${errorMsg}`);
      navigate('/upload');
    }
  });

  useEffect(() => {
    if (!taskId) {
      navigate('/upload');
    }
  }, [taskId, navigate]);

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900/20 to-cyan-900/20 flex items-center justify-center px-4">
        <div className="text-center text-red-400">
          <i className="ri-error-warning-line text-5xl mb-4"></i>
          <p className="text-lg sm:text-xl">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative min-h-screen bg-black overflow-hidden">
      {/* 배경 이미지 */}
      <div className="absolute inset-0">
        <img
          src="/img/exhibition_background.png"
          className="w-full h-full object-cover"
          alt="background"
        />
      </div>

      {/* 블랙 오버레이 */}
      <div className="absolute inset-0 bg-black opacity-50" />

      {/* 실제 내용 */}
      <div className="relative z-10 flex flex-col min-h-screen">
        <Navigation />

        {/* 중앙 정렬 영역 */}
        <div className="flex-grow flex items-center justify-center px-4 sm:px-6">
          <LoadingProgress taskId={taskId} progress={progress} />
        </div>
      </div>

      {/* Background Effects */}
      <div className="fixed top-1/4 left-4 sm:left-10 w-16 sm:w-20 h-16 sm:h-20 bg-gradient-to-br from-purple-500/20 to-cyan-500/20 rounded-full blur-xl animate-pulse" />
      <div className="fixed bottom-1/4 right-4 sm:right-10 w-24 sm:w-32 h-24 sm:h-32 bg-gradient-to-br from-cyan-500/10 to-purple-500/10 rounded-full blur-2xl animate-pulse animation-delay-700" />
      <div className="fixed top-1/2 right-4 sm:right-20 w-12 sm:w-16 h-12 sm:h-16 bg-gradient-to-br from-pink-500/30 to-purple-500/30 rounded-full blur-lg animate-pulse animation-delay-300" />
    </div>
  );
}