from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .models import UserProfile
from .serializers import (
    UserLoginSerializer, UserProfileSerializer,
    UserRegistrationSerializer, UserDetailSerializer, UserUpdateSerializer,
    PasswordChangeSerializer
)
import json
import requests
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
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name
                },
                'token': 'session-token'
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
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return Response({
                    'message': '로그인되었습니다.',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name
                    },
                    'token': 'session-token'
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
    
    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'date_joined': user.date_joined
        }, status=status.HTTP_200_OK)


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


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_csrf_token(request):
    """CSRF 토큰 가져오기 API"""
    from django.middleware.csrf import get_token
    csrf_token = get_token(request)
    return Response({
        'csrfToken': csrf_token
    }, status=status.HTTP_200_OK)


class GoogleLoginView(APIView):
    """Google OAuth 로그인 API"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            credential = request.data.get('credential')
            print(f"Received Google credential: {credential[:50]}...")
            
            if not credential:
                return Response({
                    'error': 'Google credential is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Google ID Token을 검증하고 사용자 정보 추출
            print("Validating Google credential...")
            google_response = requests.get(
                f'https://oauth2.googleapis.com/tokeninfo?id_token={credential}'
            )
            
            print(f"Google API response status: {google_response.status_code}")
            
            if google_response.status_code != 200:
                print(f"Google API error: {google_response.text}")
                return Response({
                    'error': 'Invalid Google credential'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            google_data = google_response.json()
            print(f"Google user data: {google_data}")
            
            email = google_data.get('email')
            name = google_data.get('name')
            
            if not email:
                return Response({
                    'error': 'Email not provided by Google'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            print(f"Processing user with email: {email}")
            
            # 사용자가 이미 존재하는지 확인
            try:
                user = User.objects.get(email=email)
                print(f"Existing user found: {user.username}")
                
                # 기존 사용자의 경우 UserProfile이 없으면 생성
                if not hasattr(user, 'profile'):
                    print(f"Creating profile for existing user: {user.username}")
                    UserProfile.objects.create(
                        user=user,
                        is_verified=True
                    )
                    
            except User.DoesNotExist:
                # 새 사용자 생성
                username = email.split('@')[0]  # 이메일에서 사용자명 생성
                # 사용자명 중복 방지
                counter = 1
                original_username = username
                while User.objects.filter(username=username).exists():
                    username = f"{original_username}{counter}"
                    counter += 1
                
                print(f"Creating new user: {username}")
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=name or '',
                    password=None  # Google 로그인은 비밀번호가 없음
                )
                user.is_active = True
                user.save()
                
                # UserProfile은 post_save 시그널에 의해 자동 생성되지만, 
                # 확실히 하기 위해 한 번 더 확인
                if not hasattr(user, 'profile'):
                    print(f"Creating profile for new user: {user.username}")
                    UserProfile.objects.create(
                        user=user,
                        is_verified=True
                    )
                print(f"New user created successfully: {user.username}")
            
            # 로그인 처리 (Django 기본 백엔드 사용)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            print(f"User logged in successfully: {user.username}")
            
            return Response({
                'message': 'Google 로그인 성공',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name
                },
                'token': 'google-auth-token'  # 세션 기반 인증이므로 토큰은 필요 없음
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Google login error: {str(e)}")
            return Response({
                'error': f'Google login failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GoogleCallbackView(View):
    """Google OAuth 콜백 처리"""
    
    def get(self, request):
        """Google OAuth 콜백 후 프론트엔드로 리다이렉트"""
        from django.conf import settings
        
        # 프론트엔드 URL로 리다이렉트
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        
        # 로그인 성공 시 대시보드로, 실패 시 로그인 페이지로
        if request.user.is_authenticated:
            redirect_url = f"{frontend_url}/dashboard"
        else:
            redirect_url = f"{frontend_url}/login?error=google_auth_failed"
        
        return JsonResponse({
            'redirect_url': redirect_url
        })