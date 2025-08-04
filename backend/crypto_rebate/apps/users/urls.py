from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # 인증 관련
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    path('auth/logout/', views.UserLogoutView.as_view(), name='logout'),
    
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
] 