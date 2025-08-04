from django.urls import path
from . import views

app_name = 'rebates'

urlpatterns = [
    # 페이백 내역
    path('list/', views.RebateListView.as_view(), name='rebate_list'),
    path('detail/<int:pk>/', views.RebateDetailView.as_view(), name='rebate_detail'),
    
    # 페이백 지급 내역
    path('payment/list/', views.RebatePaymentListView.as_view(), name='payment_list'),
    
    # 사용자 페이백 요약
    path('summary/', views.UserRebateSummaryListView.as_view(), name='summary_list'),
    
    # 페이백 요청 및 계산
    path('request/', views.request_rebate, name='request_rebate'),
    path('calculate/', views.calculate_rebate, name='calculate_rebate'),
    path('cancel/', views.cancel_rebate_request, name='cancel_request'),
    
    # 통계 및 대시보드
    path('stats/', views.rebate_stats, name='stats'),
    path('dashboard/', views.rebate_dashboard, name='dashboard'),
    path('history/', views.rebate_history, name='history'),
] 