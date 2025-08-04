from rest_framework import serializers
from .models import DailyStatistics, ExchangeStatistics, UserActivity, SystemMetrics


class DailyStatisticsSerializer(serializers.ModelSerializer):
    """일일 통계 시리얼라이저"""
    
    class Meta:
        model = DailyStatistics
        fields = [
            'id', 'user', 'date', 'total_earnings', 'transaction_count',
            'active_exchanges', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ExchangeStatisticsSerializer(serializers.ModelSerializer):
    """거래소 통계 시리얼라이저"""
    exchange_name = serializers.CharField(source='exchange.name', read_only=True)
    
    class Meta:
        model = ExchangeStatistics
        fields = [
            'id', 'user', 'exchange', 'exchange_name', 'date',
            'total_earnings', 'transaction_count', 'commission_rate',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserActivitySerializer(serializers.ModelSerializer):
    """사용자 활동 시리얼라이저"""
    
    class Meta:
        model = UserActivity
        fields = [
            'id', 'user', 'activity_type', 'description', 'ip_address',
            'user_agent', 'timestamp'
        ]
        read_only_fields = ['id', 'user', 'timestamp']


class SystemMetricsSerializer(serializers.ModelSerializer):
    """시스템 메트릭 시리얼라이저"""
    
    class Meta:
        model = SystemMetrics
        fields = [
            'id', 'user', 'metric_type', 'value', 'unit', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class AnalyticsDashboardSerializer(serializers.Serializer):
    """분석 대시보드 시리얼라이저"""
    total_earnings = serializers.DecimalField(max_digits=10, decimal_places=2)
    monthly_earnings = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_transactions = serializers.IntegerField()
    active_exchanges = serializers.IntegerField()
    exchange_breakdown = serializers.DictField()
    recent_activities = serializers.ListField()


class AnalyticsStatsSerializer(serializers.Serializer):
    """분석 통계 시리얼라이저"""
    period = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    daily_stats = serializers.ListField()
    exchange_stats = serializers.ListField()
    user_activity = serializers.ListField() 