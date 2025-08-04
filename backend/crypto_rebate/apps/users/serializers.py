from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import models
from .models import UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """사용자 프로필 시리얼라이저"""
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'phone_number', 'country', 'timezone',
            'preferred_currency', 'notification_settings', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """회원가입 시리얼라이저"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'profile'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return attrs
    
    def create(self, validated_data):
        password_confirm = validated_data.pop('password_confirm')
        profile_data = validated_data.pop('profile', {})
        
        user = User.objects.create_user(**validated_data)
        
        # 프로필 생성
        UserProfile.objects.create(user=user, **profile_data)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """로그인 시리얼라이저"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserDetailSerializer(serializers.ModelSerializer):
    """사용자 상세 정보 시리얼라이저"""
    profile = UserProfileSerializer(read_only=True)
    total_earnings = serializers.SerializerMethodField()
    active_exchanges = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'date_joined', 'last_login', 'is_active', 'profile',
            'total_earnings', 'active_exchanges'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def get_total_earnings(self, obj):
        """총 수익 계산"""
        from crypto_rebate.apps.rebates.models import Rebate
        return Rebate.objects.filter(user=obj, status='paid').aggregate(
            total=models.Sum('amount')
        )['total'] or 0
    
    def get_active_exchanges(self, obj):
        """활성 거래소 수"""
        from crypto_rebate.apps.exchanges.models import ExchangeAPI
        return ExchangeAPI.objects.filter(user=obj, is_active=True).count()


class UserUpdateSerializer(serializers.ModelSerializer):
    """사용자 정보 수정 시리얼라이저"""
    profile = UserProfileSerializer(partial=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile']
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        # 사용자 정보 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # 프로필 정보 업데이트
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    """비밀번호 변경 시리얼라이저"""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("새 비밀번호가 일치하지 않습니다.")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("현재 비밀번호가 올바르지 않습니다.")
        return value 