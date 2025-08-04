from django.urls import path
from . import views

app_name = 'exchanges'

urlpatterns = [
    # 거래소 정보
    path('list/', views.ExchangeListView.as_view(), name='exchange_list'),
    path('detail/<int:pk>/', views.ExchangeDetailView.as_view(), name='exchange_detail'),
    
    # 사용자별 리베이트 비율 관리
    path('rebate-rates/', views.UserExchangeRebateRateListView.as_view(), name='user_rebate_rates'),
    path('rebate-rates/<int:pk>/', views.UserExchangeRebateRateDetailView.as_view(), name='user_rebate_rate_detail'),
    path('rebate-rates/create/', views.create_user_rebate_rate, name='create_user_rebate_rate'),
    path('rebate-rates/<int:exchange_id>/update/', views.update_user_rebate_rate, name='update_user_rebate_rate'),
    
    # 사용자 거래소 API 연동
    path('api/list/', views.UserExchangeAPIListView.as_view(), name='user_api_list'),
    path('api/detail/<int:pk>/', views.UserExchangeAPIDetailView.as_view(), name='user_api_detail'),
    
    # 레퍼럴 링크
    path('referral/list/', views.ReferralLinkListView.as_view(), name='referral_list'),
    path('referral/detail/<int:pk>/', views.ReferralLinkDetailView.as_view(), name='referral_detail'),
    
    # 거래 내역
    path('transaction/list/', views.ReferralTransactionListView.as_view(), name='transaction_list'),
    path('transaction/detail/<int:pk>/', views.ReferralTransactionDetailView.as_view(), name='transaction_detail'),
    
    # 연동 가이드
    path('guides/', views.exchange_integration_guides, name='integration_guides'),
    
    # 통계 및 대시보드
    path('stats/', views.user_exchange_stats, name='user_stats'),
    path('dashboard/', views.exchange_dashboard, name='dashboard'),
    
    # API 테스트 및 동기화
    path('test-api/', views.test_exchange_api, name='test_api'),
    path('sync/', views.sync_exchange_data, name='sync_data'),
] 