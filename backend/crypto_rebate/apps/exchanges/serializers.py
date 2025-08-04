from rest_framework import serializers
from .models import Exchange, UserExchangeRebateRate, ExchangeAPI, ReferralLink, ReferralTransaction


class ExchangeSerializer(serializers.ModelSerializer):
    """거래소 정보 시리얼라이저"""
    
    class Meta:
        model = Exchange
        fields = [
            'id', 'name', 'logo', 'website', 'api_documentation',
            'base_rebate_rate', 'base_rebate_rate_percentage', 'min_withdrawal', 
            'supported_countries', 'features', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserExchangeRebateRateSerializer(serializers.ModelSerializer):
    """사용자별 거래소 리베이트 비율 시리얼라이저"""
    exchange_name = serializers.CharField(source='exchange.name', read_only=True)
    exchange_logo = serializers.CharField(source='exchange.logo', read_only=True)
    base_rebate_rate_percentage = serializers.DecimalField(source='exchange.base_rebate_rate_percentage', read_only=True, max_digits=5, decimal_places=2)
    effective_rebate_rate_percentage = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)
    
    class Meta:
        model = UserExchangeRebateRate
        fields = [
            'id', 'user', 'exchange', 'exchange_name', 'exchange_logo',
            'custom_rebate_rate', 'custom_rebate_rate_percentage',
            'base_rebate_rate_percentage', 'effective_rebate_rate_percentage',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ExchangeAPISerializer(serializers.ModelSerializer):
    """거래소 API 연동 시리얼라이저"""
    exchange_name = serializers.CharField(source='exchange.name', read_only=True)
    exchange_logo = serializers.CharField(source='exchange.logo', read_only=True)
    effective_rebate_rate_percentage = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)
    
    class Meta:
        model = ExchangeAPI
        fields = [
            'id', 'user', 'exchange', 'exchange_name', 'exchange_logo',
            'api_key', 'api_secret', 'passphrase', 'effective_rebate_rate_percentage',
            'is_active', 'last_sync', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'last_sync', 'created_at', 'updated_at']
        extra_kwargs = {
            'api_key': {'write_only': True},
            'api_secret': {'write_only': True},
            'passphrase': {'write_only': True}
        }
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ExchangeAPICreateSerializer(serializers.ModelSerializer):
    """거래소 API 연동 생성 시리얼라이저"""
    exchange_name = serializers.CharField(source='exchange.name', read_only=True)
    exchange_logo = serializers.CharField(source='exchange.logo', read_only=True)
    effective_rebate_rate_percentage = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)
    
    class Meta:
        model = ExchangeAPI
        fields = [
            'id', 'exchange', 'exchange_name', 'exchange_logo',
            'api_key', 'api_secret', 'passphrase', 'effective_rebate_rate_percentage',
            'is_active', 'last_sync', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'last_sync', 'created_at', 'updated_at']
        extra_kwargs = {
            'api_key': {'write_only': True},
            'api_secret': {'write_only': True},
            'passphrase': {'write_only': True}
        }
    
    def validate(self, attrs):
        user = self.context['request'].user
        exchange = attrs['exchange']
        
        # 이미 연동된 거래소인지 확인
        if ExchangeAPI.objects.filter(user=user, exchange=exchange).exists():
            raise serializers.ValidationError("이미 연동된 거래소입니다.")
        
        return attrs
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ReferralLinkSerializer(serializers.ModelSerializer):
    """레퍼럴 링크 시리얼라이저"""
    exchange_name = serializers.CharField(source='exchange.name', read_only=True)
    exchange_logo = serializers.CharField(source='exchange.logo', read_only=True)
    effective_rebate_rate_percentage = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)
    
    class Meta:
        model = ReferralLink
        fields = [
            'id', 'user', 'exchange', 'exchange_name', 'exchange_logo',
            'referral_code', 'referral_link', 'clicks', 'conversions',
            'total_commission', 'effective_rebate_rate_percentage',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'clicks', 'conversions', 'total_commission', 'created_at', 'updated_at']


class ReferralTransactionSerializer(serializers.ModelSerializer):
    """레퍼럴 거래 내역 시리얼라이저"""
    exchange_name = serializers.CharField(source='exchange.name', read_only=True)
    effective_rebate_rate_percentage = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)
    calculated_rebate_amount = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    
    class Meta:
        model = ReferralTransaction
        fields = [
            'id', 'user', 'exchange', 'exchange_name', 'referral_link',
            'transaction_id', 'amount', 'commission', 'commission_rate',
            'effective_rebate_rate_percentage', 'calculated_rebate_amount',
            'status', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class ExchangeIntegrationGuideSerializer(serializers.Serializer):
    """거래소 연동 가이드 시리얼라이저"""
    exchange_id = serializers.IntegerField()
    exchange_name = serializers.CharField()
    logo = serializers.CharField()
    base_rebate_rate_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
    min_withdrawal = serializers.DecimalField(max_digits=10, decimal_places=2)
    steps = serializers.ListField(child=serializers.CharField())
    video_url = serializers.CharField(required=False)
    highlight = serializers.CharField(required=False)
    api_fields = serializers.ListField(child=serializers.CharField())


class ExchangeStatsSerializer(serializers.Serializer):
    """거래소 통계 시리얼라이저"""
    exchange_name = serializers.CharField()
    total_commission = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_rebate = serializers.DecimalField(max_digits=10, decimal_places=2)
    transaction_count = serializers.IntegerField()
    last_transaction = serializers.DateTimeField(required=False)
    is_active = serializers.BooleanField()
    effective_rebate_rate_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)


class ExchangeAPITestSerializer(serializers.Serializer):
    """거래소 API 테스트 시리얼라이저"""
    exchange_id = serializers.IntegerField()
    api_key = serializers.CharField()
    api_secret = serializers.CharField()
    passphrase = serializers.CharField(required=False)
    
    def validate(self, attrs):
        exchange_id = attrs['exchange_id']
        try:
            exchange = Exchange.objects.get(id=exchange_id, is_active=True)
        except Exchange.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 거래소입니다.")
        
        attrs['exchange'] = exchange
        return attrs


class ExchangeSyncSerializer(serializers.Serializer):
    """거래소 동기화 시리얼라이저"""
    exchange_api_id = serializers.IntegerField()
    sync_type = serializers.ChoiceField(choices=['transactions', 'commissions', 'all'])
    
    def validate(self, attrs):
        exchange_api_id = attrs['exchange_api_id']
        user = self.context['request'].user
        
        try:
            exchange_api = ExchangeAPI.objects.get(
                id=exchange_api_id, 
                user=user, 
                is_active=True
            )
        except ExchangeAPI.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 거래소 API입니다.")
        
        attrs['exchange_api'] = exchange_api
        return attrs


class UserRebateRateUpdateSerializer(serializers.ModelSerializer):
    """사용자 리베이트 비율 업데이트 시리얼라이저"""
    
    class Meta:
        model = UserExchangeRebateRate
        fields = ['custom_rebate_rate', 'is_active']
    
    def validate_custom_rebate_rate(self, value):
        """리베이트 비율 검증"""
        if value < 0 or value > 1:
            raise serializers.ValidationError("리베이트 비율은 0과 1 사이의 값이어야 합니다.")
        return value 