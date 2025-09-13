import axios from 'axios';
import { environment } from '../config/environment';

// API 기본 설정
const api = axios.create({
  baseURL: environment.apiUrl,
  withCredentials: true, // 세션 기반 인증을 위해 항상 true
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터
api.interceptors.request.use(
  async (config) => {
    // CSRF 토큰 가져오기
    if (config.method !== 'get') {
      try {
        const csrfResponse = await axios.get(`${environment.apiUrl}/api/v1/csrf/`, {
          withCredentials: true
        });
        config.headers['X-CSRFToken'] = csrfResponse.data.csrfToken;
      } catch (error) {
        console.warn('CSRF token could not be retrieved:', error);
      }
    }
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