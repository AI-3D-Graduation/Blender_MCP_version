/**
 * 진행률에 따른 적응형 폴링 간격 계산
 */
export const getAdaptivePollingInterval = (progress: number): number => {
  if (progress < 30) return 5000;   // 초반: 5초
  if (progress < 70) return 10000;  // 중반: 10초
  if (progress < 95) return 5000;   // 후반: 5초
  return 2000;                      // 거의 완료: 2초
};

/**
 * 진행률에 따른 현재 단계 계산
 */
export const calculateCurrentStep = (progress: number): number => {
  if (progress < 25) return 0;
  if (progress < 50) return 1;
  if (progress < 75) return 2;
  return 3;
};

/**
 * 남은 예상 시간 계산 (초)
 */
export const calculateEstimatedTime = (progress: number): number => {
  return Math.max(0, Math.ceil((100 - progress) * 0.6));
};