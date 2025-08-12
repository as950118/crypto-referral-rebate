// 환경별 API URL 설정
const getApiUrl = () => {
  if (process.env.NODE_ENV === 'production') {
    // 프로덕션 환경에서는 실제 백엔드 URL 사용
    return process.env.REACT_APP_API_URL || 'https://your-backend-domain.com';
  }
  // 개발 환경에서는 로컬 백엔드 사용
  return 'http://localhost:8000';
};

export const API_BASE_URL = getApiUrl();
export const IS_PRODUCTION = process.env.NODE_ENV === 'production'; 