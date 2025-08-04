from rest_framework import serializers
from django.db import models
from .models import RebatePolicy, Rebate, RebatePayment, UserRebateSummary


class RebatePolicySerializer(serializers.ModelSerializer):
    """페이백 정책 시리얼라이저"""
    
    class Meta:
        model = RebatePolicy
        fields = [
            'id', 'exchange', 'rebate_rate', 'min_volume', 'max_volume',
            'tier_level', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RebateSerializer(serializers.ModelSerializer):
    """페이백 내역 시리얼라이저"""
    exchange_name = serializers.CharField(source='exchange.name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Rebate
        fields = [
            'id', 'user', 'user_username', 'exchange', 'exchange_name',
            'referral_transaction', 'amount', 'rebate_rate', 'status',
            'payment_method', 'payment_address', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class RebatePaymentSerializer(serializers.ModelSerializer):
    """페이백 지급 내역 시리얼라이저"""
    rebate_exchange = serializers.CharField(source='rebate.exchange.name', read_only=True)
    
    class Meta:
        model = RebatePayment
        fields = [
            'id', 'rebate', 'rebate_exchange', 'amount', 'payment_method',
            'payment_address', 'transaction_hash', 'status', 'processed_at',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserRebateSummarySerializer(serializers.ModelSerializer):
    """사용자 페이백 요약 시리얼라이저"""
    exchange_name = serializers.CharField(source='exchange.name', read_only=True)
    
    class Meta:
        model = UserRebateSummary
        fields = [
            'id', 'user', 'exchange', 'exchange_name', 'total_commission',
            'total_rebate', 'pending_rebate', 'paid_rebate', 'transaction_count',
            'last_updated'
        ]
        read_only_fields = ['id', 'last_updated']


class RebateRequestSerializer(serializers.Serializer):
    """페이백 요청 시리얼라이저"""
    exchange_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.ChoiceField(choices=[
        ('usdt', 'USDT'),
        ('btc', 'BTC'),
        ('eth', 'ETH'),
        ('bank', '은행이체'),
        ('paypal', 'PayPal')
    ])
    payment_address = serializers.CharField(required=False)
    
    def validate(self, attrs):
        user = self.context['request'].user
        exchange_id = attrs['exchange_id']
        amount = attrs['amount']
        
        # 거래소 확인
        from crypto_rebate.apps.exchanges.models import Exchange
        try:
            exchange = Exchange.objects.get(id=exchange_id, is_active=True)
        except Exchange.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 거래소입니다.")
        
        # 사용자의 해당 거래소 페이백 확인
        from .models import Rebate
        available_rebate = Rebate.objects.filter(
            user=user, exchange=exchange, status='pending'
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
        if amount > available_rebate:
            raise serializers.ValidationError("요청 금액이 사용 가능한 페이백보다 큽니다.")
        
        attrs['exchange'] = exchange
        return attrs


class RebateStatsSerializer(serializers.Serializer):
    """페이백 통계 시리얼라이저"""
    total_earnings = serializers.DecimalField(max_digits=10, decimal_places=2)
    monthly_earnings = serializers.DecimalField(max_digits=10, decimal_places=2)
    pending_rebates = serializers.DecimalField(max_digits=10, decimal_places=2)
    paid_rebates = serializers.DecimalField(max_digits=10, decimal_places=2)
    exchange_breakdown = serializers.DictField()
    recent_rebates = serializers.ListField()


class RebateCalculatorSerializer(serializers.Serializer):
    """페이백 계산기 시리얼라이저"""
    exchange_id = serializers.IntegerField()
    commission_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    def validate(self, attrs):
        exchange_id = attrs['exchange_id']
        
        # 거래소 확인
        from crypto_rebate.apps.exchanges.models import Exchange
        try:
            exchange = Exchange.objects.get(id=exchange_id, is_active=True)
        except Exchange.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 거래소입니다.")
        
        attrs['exchange'] = exchange
        return attrs
    
    def calculate_rebate(self):
        """페이백 계산"""
        exchange = self.validated_data['exchange']
        commission_amount = self.validated_data['commission_amount']
        
        # 거래소별 페이백 비율
        rebate_rates = {
            'Binance': 0.45,  # 45%
            'Bybit': 0.40,    # 40%
            'OKX': 0.35,      # 35%
            'Gate.io': 0.30   # 30%
        }
        
        rebate_rate = rebate_rates.get(exchange.name, 0.20)
        rebate_amount = commission_amount * rebate_rate
        
        return {
            'exchange': exchange.name,
            'commission_amount': commission_amount,
            'rebate_rate': rebate_rate,
            'rebate_amount': rebate_amount
        } 