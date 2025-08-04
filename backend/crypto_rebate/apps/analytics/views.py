from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import DailyStatistics, ExchangeStatistics, UserActivity, SystemMetrics


# Create your views here.


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def analytics_dashboard(request):
    """분석 대시보드 API"""
    user = request.user
    
    # 오늘 통계
    today = timezone.now().date()
    today_stats = DailyStatistics.objects.filter(
        user=user, date=today
    ).first()
    
    # 이번 주 통계
    week_start = today - timedelta(days=today.weekday())
    week_stats = DailyStatistics.objects.filter(
        user=user, date__gte=week_start
    ).aggregate(
        total_earnings=Sum('total_earnings'),
        total_transactions=Sum('transaction_count'),
        avg_daily_earnings=Avg('total_earnings')
    )
    
    # 이번 달 통계
    month_start = today.replace(day=1)
    month_stats = DailyStatistics.objects.filter(
        user=user, date__gte=month_start
    ).aggregate(
        total_earnings=Sum('total_earnings'),
        total_transactions=Sum('transaction_count'),
        avg_daily_earnings=Avg('total_earnings')
    )
    
    # 거래소별 통계
    exchange_stats = ExchangeStatistics.objects.filter(
        user=user
    ).values('exchange__name').annotate(
        total_earnings=Sum('total_earnings'),
        total_transactions=Sum('transaction_count')
    )
    
    return Response({
        'today': {
            'earnings': today_stats.total_earnings if today_stats else 0,
            'transactions': today_stats.transaction_count if today_stats else 0
        },
        'this_week': week_stats,
        'this_month': month_stats,
        'exchange_breakdown': list(exchange_stats)
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def analytics_stats(request):
    """분석 통계 API"""
    user = request.user
    
    # 기간 필터
    period = request.GET.get('period', 'month')  # week, month, year
    end_date = timezone.now().date()
    
    if period == 'week':
        start_date = end_date - timedelta(days=7)
    elif period == 'month':
        start_date = end_date - timedelta(days=30)
    elif period == 'year':
        start_date = end_date - timedelta(days=365)
    else:
        start_date = end_date - timedelta(days=30)
    
    # 일별 통계
    daily_stats = DailyStatistics.objects.filter(
        user=user, date__range=[start_date, end_date]
    ).order_by('date')
    
    # 거래소별 통계
    exchange_stats = ExchangeStatistics.objects.filter(
        user=user, date__range=[start_date, end_date]
    ).values('exchange__name').annotate(
        total_earnings=Sum('total_earnings'),
        total_transactions=Sum('transaction_count')
    )
    
    # 사용자 활동
    user_activity = UserActivity.objects.filter(
        user=user, timestamp__date__range=[start_date, end_date]
    ).values('activity_type').annotate(
        count=Count('id')
    )
    
    return Response({
        'period': period,
        'start_date': start_date,
        'end_date': end_date,
        'daily_stats': [
            {
                'date': stat.date,
                'earnings': stat.total_earnings,
                'transactions': stat.transaction_count
            }
            for stat in daily_stats
        ],
        'exchange_stats': list(exchange_stats),
        'user_activity': list(user_activity)
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_activity(request):
    """사용자 활동 API"""
    user = request.user
    
    # 활동 타입별 통계
    activity_stats = UserActivity.objects.filter(
        user=user
    ).values('activity_type').annotate(
        count=Count('id')
    )
    
    # 최근 활동
    recent_activities = UserActivity.objects.filter(
        user=user
    ).order_by('-timestamp')[:20]
    
    # 시간대별 활동
    hourly_activity = UserActivity.objects.filter(
        user=user,
        timestamp__date=timezone.now().date()
    ).extra(
        select={'hour': "EXTRACT(hour FROM timestamp)"}
    ).values('hour').annotate(
        count=Count('id')
    ).order_by('hour')
    
    return Response({
        'activity_stats': list(activity_stats),
        'recent_activities': [
            {
                'id': activity.id,
                'activity_type': activity.activity_type,
                'description': activity.description,
                'timestamp': activity.timestamp
            }
            for activity in recent_activities
        ],
        'hourly_activity': list(hourly_activity)
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def system_metrics(request):
    """시스템 메트릭 API"""
    user = request.user
    
    # 시스템 성능 메트릭
    system_metrics = SystemMetrics.objects.filter(
        user=user
    ).order_by('-timestamp')[:10]
    
    # API 응답 시간
    api_response_times = SystemMetrics.objects.filter(
        user=user,
        metric_type='api_response_time'
    ).order_by('-timestamp')[:20]
    
    # 오류율
    error_rates = SystemMetrics.objects.filter(
        user=user,
        metric_type='error_rate'
    ).order_by('-timestamp')[:20]
    
    return Response({
        'system_metrics': [
            {
                'id': metric.id,
                'metric_type': metric.metric_type,
                'value': metric.value,
                'timestamp': metric.timestamp
            }
            for metric in system_metrics
        ],
        'api_response_times': [
            {
                'value': metric.value,
                'timestamp': metric.timestamp
            }
            for metric in api_response_times
        ],
        'error_rates': [
            {
                'value': metric.value,
                'timestamp': metric.timestamp
            }
            for metric in error_rates
        ]
    }, status=status.HTTP_200_OK)
