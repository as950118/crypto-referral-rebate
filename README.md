# Crypto Referral Rebate Platform

코인 거래소의 레퍼럴 수수료를 자동으로 페이백해주는 플랫폼입니다.

## 🎯 프로젝트 개요

이 플랫폼은 사용자들이 거래소에서 발생하는 레퍼럴 수수료를 자동으로 추적하고, 설정된 조건에 따라 페이백을 제공하는 서비스입니다.

## 📋 주요 기능

### 1. 사용자 관리
- 회원가입/로그인 시스템
- 사용자 프로필 관리
- 레퍼럴 링크 생성 및 관리
- 수수료 추적 대시보드

### 2. 거래소 연동
- 주요 거래소 API 연동 (Binance, Upbit, Bithumb 등)
- 실시간 거래 데이터 수집
- 레퍼럴 수수료 자동 계산
- 거래 내역 추적

### 3. 페이백 시스템
- 수수료 페이백 조건 설정
- 자동 페이백 처리
- 페이백 내역 관리
- 수수료 정산 시스템

### 4. 관리자 기능
- 사용자 관리
- 거래소 설정 관리
- 페이백 정책 설정
- 통계 및 분석 대시보드

## 🛠 기술 스택

### Frontend
- **React.js** - 사용자 인터페이스
- **TypeScript** - 타입 안정성
- **Tailwind CSS** - 스타일링
- **Redux Toolkit** - 상태 관리
- **React Query** - 서버 상태 관리

### Backend
- **Django** - 웹 프레임워크
- **Django REST Framework** - API 개발
- **Django Admin** - 관리자 패널
- **PostgreSQL** - 데이터베이스
- **Celery** - 비동기 작업 처리

### 인프라
- **Docker** - 컨테이너화
- **AWS/Cloudflare** - 클라우드 호스팅
- **Redis** - 캐싱 및 세션 관리
- **JWT** - 인증 토큰

### 외부 서비스
- **거래소 APIs** - Binance, Upbit, Bithumb 등
- **결제 시스템** - Stripe, PayPal 등
- **이메일 서비스** - SendGrid, AWS SES
- **모니터링** - Sentry, DataDog

## 📁 프로젝트 구조

```
crypto-referral-rebate/
├── frontend/                 # React 프론트엔드
│   ├── src/
│   │   ├── components/      # 재사용 가능한 컴포넌트
│   │   ├── pages/          # 페이지 컴포넌트
│   │   ├── hooks/          # 커스텀 훅
│   │   ├── store/          # Redux 스토어
│   │   ├── services/       # API 서비스
│   │   └── utils/          # 유틸리티 함수
│   └── public/             # 정적 파일
├── backend/                 # Django 백엔드
│   ├── crypto_rebate/       # Django 프로젝트
│   │   ├── manage.py        # Django 관리 스크립트
│   │   ├── crypto_rebate/   # 프로젝트 설정
│   │   │   ├── settings.py  # 설정 파일
│   │   │   ├── urls.py      # 메인 URL 설정
│   │   │   └── wsgi.py      # WSGI 설정
│   │   ├── apps/            # Django 앱들
│   │   │   ├── users/       # 사용자 관리 앱
│   │   │   ├── exchanges/   # 거래소 연동 앱
│   │   │   ├── rebates/     # 페이백 관리 앱
│   │   │   └── analytics/   # 분석 앱
│   │   ├── templates/       # Django 템플릿
│   │   ├── static/          # 정적 파일
│   │   └── media/           # 업로드 파일
│   ├── requirements.txt     # Python 의존성
│   └── celery.py           # Celery 설정
├── shared/                  # 공유 타입 및 유틸리티
├── docs/                    # 문서
└── docker/                  # Docker 설정
```

## 🗄 데이터베이스 스키마

### 주요 Django 앱 및 모델
- **users** - 사용자 정보 (User, Profile)
- **exchanges** - 거래소 정보 (Exchange, ExchangeAPI)
- **referrals** - 레퍼럴 링크 (ReferralLink, ReferralTransaction)
- **transactions** - 거래 내역 (Transaction, TradeHistory)
- **rebates** - 페이백 내역 (Rebate, RebatePolicy)
- **analytics** - 분석 데이터 (Analytics, Statistics)

## 🔐 보안 고려사항

### API 보안
- Django Session 기반 인증
- Django REST Framework JWT 토큰
- API 키 암호화 저장 (Fernet)
- Django Rate Limiting
- CORS 설정 (django-cors-headers)

### 데이터 보안
- 개인정보 암호화
- 거래소 API 키 보안 관리
- 로그 보안 처리

## 📊 모니터링 및 분석

### 성능 모니터링
- 서버 응답 시간
- 데이터베이스 쿼리 성능
- API 호출 빈도

### 비즈니스 분석
- 사용자 활동 추적
- 페이백 통계
- 거래소별 수수료 분석

## 🚀 배포 전략

### 개발 환경
- Docker Compose로 로컬 개발 환경 구성
- Django 개발 서버 (Hot reload 지원)
- SQLite 개발용 데이터베이스
- Django Debug Toolbar

### 프로덕션 환경
- CI/CD 파이프라인 구축
- Blue-Green 배포
- 자동 스케일링
- 백업 및 복구 시스템

## 📈 수익 모델

### 수수료 구조
- 플랫폼 수수료 (페이백 금액의 일정 비율)
- 프리미엄 서비스 요금
- API 사용료

### 비즈니스 모델
- Freemium 모델
- 월 구독 서비스
- 성과 기반 수수료

## 🔄 개발 로드맵

### Phase 1: MVP (2-3개월)
- Django 프로젝트 설정
- 기본 사용자 관리 (Django Admin 활용)
- 단일 거래소 연동 (Binance API)
- 기본 페이백 시스템
- Django REST Framework API 개발

### Phase 2: 확장 (3-4개월)
- 다중 거래소 지원
- 고급 분석 기능
- 모바일 앱 개발

### Phase 3: 고도화 (4-6개월)
- AI 기반 수수료 최적화
- 글로벌 서비스 확장
- 파트너십 프로그램

## 🛡️ 법적 고려사항

### 규제 준수
- 금융 규제 준수
- 개인정보보호법 준수
- 세무 신고 시스템

### 이용약관
- 서비스 이용약관
- 개인정보처리방침
- 수수료 정책

## 📞 지원 및 문의

- 이메일: support@cryptorebate.com
- 기술 문서: [Wiki 링크]
- 커뮤니티: [Discord 링크]

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

**참고**: 이 문서는 프로젝트 초기 기획 단계에서 작성되었으며, 개발 과정에서 지속적으로 업데이트됩니다.