# Google OAuth 설정 가이드

이 가이드는 Crypto Referral Rebate 프로젝트에서 Google OAuth 로그인을 설정하는 방법을 설명합니다.

## 1. Google Cloud Console 설정

### 1.1 프로젝트 생성
1. [Google Cloud Console](https://console.cloud.google.com/)에 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택

### 1.2 OAuth 2.0 클라이언트 ID 생성
1. "API 및 서비스" > "사용자 인증 정보"로 이동
2. "사용자 인증 정보 만들기" > "OAuth 2.0 클라이언트 ID" 선택
3. 애플리케이션 유형: "웹 애플리케이션" 선택
4. 이름 입력 (예: "Crypto Rebate App")

### 1.3 승인된 리디렉션 URI 설정
다음 URI들을 추가:
```
http://localhost:3000
http://localhost:8000/accounts/google/login/callback/
http://127.0.0.1:3000
http://127.0.0.1:8000/accounts/google/login/callback/
```

프로덕션 환경의 경우:
```
https://yourdomain.com
https://yourdomain.com/accounts/google/login/callback/
```

### 1.4 클라이언트 ID와 시크릿 복사
- 클라이언트 ID와 클라이언트 시크릿을 안전한 곳에 저장

## 2. 백엔드 설정

### 2.1 환경 변수 설정
`backend/.env` 파일을 생성하고 다음 내용을 추가:

```env
# Google OAuth Settings
GOOGLE_OAUTH2_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-google-client-secret

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Other settings...
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 2.2 패키지 설치
```bash
cd backend
pip install -r requirements.txt
```

### 2.3 데이터베이스 마이그레이션
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2.4 Django Admin에서 Social Application 설정
1. Django 서버 실행: `python manage.py runserver`
2. http://localhost:8000/admin 접속
3. "Social Applications" > "Social applications" > "Add social application"
4. Provider: Google 선택
5. Name: "Google OAuth" 입력
6. Client id: Google에서 받은 클라이언트 ID 입력
7. Secret key: Google에서 받은 클라이언트 시크릿 입력
8. Sites: "example.com" 선택 후 저장

## 3. 프론트엔드 설정

### 3.1 환경 변수 설정
`frontend/.env` 파일을 생성하고 다음 내용을 추가:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id
```

### 3.2 패키지 설치
```bash
cd frontend
npm install
```

## 4. 실행 방법

### 4.1 백엔드 실행
```bash
cd backend
python manage.py runserver
```

### 4.2 프론트엔드 실행
```bash
cd frontend
npm start
```

## 5. 테스트

1. http://localhost:3000 접속
2. "로그인" 버튼 클릭
3. "Google로 계속하기" 버튼 클릭
4. Google 계정으로 로그인
5. 대시보드로 리디렉션되는지 확인

## 6. 문제 해결

### 6.1 "redirect_uri_mismatch" 오류
- Google Cloud Console에서 승인된 리디렉션 URI가 정확한지 확인
- 도메인과 포트가 정확한지 확인

### 6.2 "invalid_client" 오류
- 클라이언트 ID와 시크릿이 정확한지 확인
- Django Admin의 Social Application 설정 확인

### 6.3 CORS 오류
- Django settings.py의 CORS_ALLOWED_ORIGINS 설정 확인
- 프론트엔드 URL이 포함되어 있는지 확인

## 7. 보안 고려사항

1. **환경 변수 보안**: `.env` 파일을 `.gitignore`에 추가
2. **HTTPS 사용**: 프로덕션 환경에서는 반드시 HTTPS 사용
3. **도메인 제한**: Google OAuth 설정에서 승인된 도메인만 허용
4. **시크릿 관리**: 클라이언트 시크릿을 안전하게 보관

## 8. 추가 기능

### 8.1 사용자 프로필 연동
Google 로그인 시 자동으로 사용자 프로필이 생성되며, 다음 정보가 저장됩니다:
- 이메일 주소
- 이름
- 프로필 사진 (Google에서 제공하는 경우)

### 8.2 로그아웃 처리
Google 로그아웃 시 Django 세션도 함께 종료됩니다.

### 8.3 에러 처리
Google 로그인 실패 시 적절한 에러 메시지가 표시됩니다.
