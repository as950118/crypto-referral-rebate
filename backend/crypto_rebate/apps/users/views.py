from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserDetailSerializer,
    UserUpdateSerializer, PasswordChangeSerializer, UserProfileSerializer
)
from .models import UserProfile
from django.db import models


# Create your views here.


class UserRegistrationView(generics.CreateAPIView):
    """회원가입 API"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': '회원가입이 완료되었습니다.',
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """로그인 API"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return Response({
                    'message': '로그인되었습니다.',
                    'user_id': user.id,
                    'username': user.username
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': '아이디 또는 비밀번호가 올바르지 않습니다.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """로그아웃 API"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({
            'message': '로그아웃되었습니다.'
        }, status=status.HTTP_200_OK)


class UserDetailView(generics.RetrieveUpdateAPIView):
    """사용자 상세 정보 조회/수정 API"""
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserUpdateView(generics.UpdateAPIView):
    """사용자 정보 수정 API"""
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class PasswordChangeView(APIView):
    """비밀번호 변경 API"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({
                'message': '비밀번호가 변경되었습니다.'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """사용자 프로필 조회/수정 API"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user.profile


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_dashboard(request):
    """사용자 대시보드 API"""
    user = request.user
    
    # 총 수익 계산
    from crypto_rebate.apps.rebates.models import Rebate
    total_earnings = Rebate.objects.filter(
        user=user, status='paid'
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    # 이번 달 수익
    from datetime import datetime
    current_month = datetime.now().month
    monthly_earnings = Rebate.objects.filter(
        user=user, status='paid', created_at__month=current_month
    ).aggregate(total=models.Sum('amount'))['total'] or 0
    
    # 활성 거래소 수
    from crypto_rebate.apps.exchanges.models import ExchangeAPI
    active_exchanges = ExchangeAPI.objects.filter(
        user=user, is_active=True
    ).count()
    
    # 최근 거래 내역
    from crypto_rebate.apps.exchanges.models import ReferralTransaction
    recent_transactions = ReferralTransaction.objects.filter(
        user=user
    ).order_by('-created_at')[:10]
    
    # 거래소별 수익
    exchange_earnings = {}
    for api in ExchangeAPI.objects.filter(user=user, is_active=True):
        earnings = Rebate.objects.filter(
            user=user, exchange=api.exchange, status='paid'
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        exchange_earnings[api.exchange.name] = earnings
    
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        },
        'statistics': {
            'total_earnings': total_earnings,
            'monthly_earnings': monthly_earnings,
            'active_exchanges': active_exchanges
        },
        'exchange_earnings': exchange_earnings,
        'recent_transactions': [
            {
                'id': tx.id,
                'exchange': tx.exchange.name,
                'amount': tx.amount,
                'commission': tx.commission,
                'created_at': tx.created_at
            }
            for tx in recent_transactions
        ]
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def check_username(request):
    """사용자명 중복 확인 API"""
    username = request.data.get('username')
    if not username:
        return Response({
            'error': '사용자명을 입력해주세요.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    exists = User.objects.filter(username=username).exists()
    return Response({
        'available': not exists,
        'message': '사용 가능한 사용자명입니다.' if not exists else '이미 사용 중인 사용자명입니다.'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def check_email(request):
    """이메일 중복 확인 API"""
    email = request.data.get('email')
    if not email:
        return Response({
            'error': '이메일을 입력해주세요.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    exists = User.objects.filter(email=email).exists()
    return Response({
        'available': not exists,
        'message': '사용 가능한 이메일입니다.' if not exists else '이미 사용 중인 이메일입니다.'
    }, status=status.HTTP_200_OK)
