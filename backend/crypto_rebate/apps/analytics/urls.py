from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # 분석 대시보드
    path('dashboard/', views.analytics_dashboard, name='dashboard'),
    
    # 통계 데이터
    path('stats/', views.analytics_stats, name='stats'),
    
    # 사용자 활동
    path('activity/', views.user_activity, name='activity'),
    
    # 시스템 메트릭
    path('metrics/', views.system_metrics, name='metrics'),
] 