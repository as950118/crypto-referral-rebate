export const environment = {
  production: false,
  apiUrl: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  googleClientId: process.env.REACT_APP_GOOGLE_CLIENT_ID || '',
}; 