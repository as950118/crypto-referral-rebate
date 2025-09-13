from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # 인증 관련
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    path('auth/logout/', views.UserLogoutView.as_view(), name='logout'),
    path('auth/google/', views.GoogleLoginView.as_view(), name='google_login'),  # Google 로그인 추가
    path('auth/google/callback/', views.GoogleCallbackView.as_view(), name='google_callback'),  # Google 콜백
    
    # 사용자 정보
    path('profile/', views.UserDetailView.as_view(), name='profile'),
    path('profile/update/', views.UserUpdateView.as_view(), name='profile_update'),
    path('profile/password/', views.PasswordChangeView.as_view(), name='password_change'),
    path('profile/details/', views.UserProfileView.as_view(), name='profile_details'),
    
    # 대시보드
    path('dashboard/', views.user_dashboard, name='dashboard'),
    
    # 중복 확인
    path('check/username/', views.check_username, name='check_username'),
    path('check/email/', views.check_email, name='check_email'),
    
    # CSRF 토큰
    path('csrf/', views.get_csrf_token, name='get_csrf_token'),
] 