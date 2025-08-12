import axios from 'axios';
import { API_BASE_URL, IS_PRODUCTION } from '../config/environment';

// API 기본 설정
const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: !IS_PRODUCTION, // 프로덕션에서는 CORS 이슈 방지
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터
api.interceptors.request.use(
  (config) => {
    // CSRF 토큰이 필요한 경우 여기서 추가
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // 인증 실패 시 로그인 페이지로 리다이렉트
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api; 