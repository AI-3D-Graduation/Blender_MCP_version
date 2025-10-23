// 환경변수 관리
// export const API_CONFIG = {
//   BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
//   TIMEOUT: 30000, // 30초
// } as const;

// 환경변수 관리
export const API_CONFIG = {
  BASE_URL: 'http://localhost:8000',
  TIMEOUT: 120000, // 120초 (2분) - Blender MCP 작업은 시간이 걸릴 수 있음
} as const;