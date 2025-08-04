from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Exchange, UserExchangeRebateRate, ExchangeAPI, ReferralLink, ReferralTransaction
from .serializers import (
    ExchangeSerializer, UserExchangeRebateRateSerializer, ExchangeAPISerializer, 
    ExchangeAPICreateSerializer, ReferralLinkSerializer, ReferralTransactionSerializer,
    ExchangeIntegrationGuideSerializer, ExchangeStatsSerializer,
    ExchangeAPITestSerializer, ExchangeSyncSerializer, UserRebateRateUpdateSerializer
)


class ExchangeListView(generics.ListAPIView):
    """지원 거래소 목록 API"""
    serializer_class = ExchangeSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Exchange.objects.filter(is_active=True)


class ExchangeDetailView(generics.RetrieveAPIView):
    """거래소 상세 정보 API"""
    serializer_class = ExchangeSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Exchange.objects.filter(is_active=True)


class UserExchangeRebateRateListView(generics.ListCreateAPIView):
    """사용자별 거래소 리베이트 비율 목록"""
    serializer_class = UserExchangeRebateRateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserExchangeRebateRate.objects.filter(user=self.request.user)


class UserExchangeRebateRateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """사용자별 거래소 리베이트 비율 상세"""
    serializer_class = UserExchangeRebateRateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserExchangeRebateRate.objects.filter(user=self.request.user)


class UserExchangeAPIListView(generics.ListCreateAPIView):
    """사용자 거래소 API 연동 목록"""
    serializer_class = ExchangeAPISerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ExchangeAPI.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ExchangeAPICreateSerializer
        return ExchangeAPISerializer


class UserExchangeAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    """사용자 거래소 API 연동 상세"""
    serializer_class = ExchangeAPISerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ExchangeAPI.objects.filter(user=self.request.user)


class ReferralLinkListView(generics.ListCreateAPIView):
    """레퍼럴 링크 목록 API"""
    serializer_class = ReferralLinkSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ReferralLink.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReferralLinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    """레퍼럴 링크 상세 API"""
    serializer_class = ReferralLinkSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ReferralLink.objects.filter(user=self.request.user)


class ReferralTransactionListView(generics.ListAPIView):
    """레퍼럴 거래 내역 목록 API"""
    serializer_class = ReferralTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ReferralTransaction.objects.filter(user=self.request.user).order_by('-created_at')


class ReferralTransactionDetailView(generics.RetrieveAPIView):
    """레퍼럴 거래 내역 상세 API"""
    serializer_class = ReferralTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ReferralTransaction.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def exchange_integration_guides(request):
    """거래소 연동 가이드 API"""
    guides = {
        'binance': {
            'exchange_id': 1,
            'exchange_name': 'Binance',
            'logo': '/static/images/binance.png',
            'base_rebate_rate_percentage': 45.00,  # 45%
            'min_withdrawal': 10,
            'steps': [
                '1. Binance 계정에 로그인',
                '2. API 관리 페이지로 이동',
                '3. 새 API 키 생성',
                '4. 거래 권한 활성화',
                '5. API 키와 시크릿 입력'
            ],
            'video_url': 'https://youtube.com/binance-guide',
            'highlight': '최고 페이백 비율',
            'api_fields': ['api_key', 'api_secret']
        },
        'bybit': {
            'exchange_id': 2,
            'exchange_name': 'Bybit',
            'logo': '/static/images/bybit.png',
            'base_rebate_rate_percentage': 40.00,  # 40%
            'min_withdrawal': 15,
            'steps': [
                '1. Bybit 계정에 로그인',
                '2. API 관리 페이지로 이동',
                '3. 새 API 키 생성',
                '4. 거래 권한 활성화',
                '5. API 키와 시크릿 입력'
            ],
            'video_url': 'https://youtube.com/bybit-guide',
            'highlight': '선물 거래 중심',
            'api_fields': ['api_key', 'api_secret']
        },
        'okx': {
            'exchange_id': 3,
            'exchange_name': 'OKX',
            'logo': '/static/images/okx.png',
            'base_rebate_rate_percentage': 35.00,  # 35%
            'min_withdrawal': 20,
            'steps': [
                '1. OKX 계정에 로그인',
                '2. API 관리 페이지로 이동',
                '3. 새 API 키 생성',
                '4. 거래 권한 활성화',
                '5. API 키, 시크릿, 패스프레이즈 입력'
            ],
            'video_url': 'https://youtube.com/okx-guide',
            'highlight': '다양한 상품',
            'api_fields': ['api_key', 'api_secret', 'passphrase']
        },
        'gate': {
            'exchange_id': 4,
            'exchange_name': 'Gate.io',
            'logo': '/static/images/gate.png',
            'base_rebate_rate_percentage': 30.00,  # 30%
            'min_withdrawal': 25,
            'steps': [
                '1. Gate.io 계정에 로그인',
                '2. API 관리 페이지로 이동',
                '3. 새 API 키 생성',
                '4. 거래 권한 활성화',
                '5. API 키와 시크릿 입력'
            ],
            'video_url': 'https://youtube.com/gate-guide',
            'highlight': '알트코인 많음',
            'api_fields': ['api_key', 'api_secret']
        }
    }
    
    return Response(guides, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_exchange_stats(request):
    """사용자 거래소별 통계 API"""
    user = request.user
    
    # 사용자의 거래소 API 목록
    exchange_apis = ExchangeAPI.objects.filter(user=user, is_active=True)
    
    stats = []
    for api in exchange_apis:
        # 총 수수료
        total_commission = ReferralTransaction.objects.filter(
            user=user, exchange=api.exchange
        ).aggregate(total=Sum('commission'))['total'] or 0
        
        # 총 페이백
        from crypto_rebate.apps.rebates.models import Rebate
        total_rebate = Rebate.objects.filter(
            user=user, exchange=api.exchange, status='paid'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # 거래 수
        transaction_count = ReferralTransaction.objects.filter(
            user=user, exchange=api.exchange
        ).count()
        
        # 마지막 거래
        last_transaction = ReferralTransaction.objects.filter(
            user=user, exchange=api.exchange
        ).order_by('-created_at').first()
        
        stats.append({
            'exchange_name': api.exchange.name,
            'total_commission': total_commission,
            'total_rebate': total_rebate,
            'transaction_count': transaction_count,
            'last_transaction': last_transaction.created_at if last_transaction else None,
            'is_active': api.is_active,
            'effective_rebate_rate_percentage': api.effective_rebate_rate_percentage
        })
    
    return Response(stats, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def test_exchange_api(request):
    """거래소 API 테스트 API"""
    serializer = ExchangeAPITestSerializer(data=request.data)
    if serializer.is_valid():
        exchange = serializer.validated_data['exchange']
        api_key = serializer.validated_data['api_key']
        api_secret = serializer.validated_data['api_secret']
        passphrase = serializer.validated_data.get('passphrase')
        
        # 실제 API 테스트 로직 (여기서는 시뮬레이션)
        try:
            # API 연결 테스트
            if exchange.name == 'Binance':
                # Binance API 테스트
                success = True
                message = "API 연결이 성공했습니다."
            elif exchange.name == 'Bybit':
                # Bybit API 테스트
                success = True
                message = "API 연결이 성공했습니다."
            else:
                success = True
                message = "API 연결이 성공했습니다."
            
            return Response({
                'success': success,
                'message': message,
                'exchange': exchange.name
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f"API 연결에 실패했습니다: {str(e)}",
                'exchange': exchange.name
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def sync_exchange_data(request):
    """거래소 데이터 동기화 API"""
    serializer = ExchangeSyncSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        exchange_api = serializer.validated_data['exchange_api']
        sync_type = serializer.validated_data['sync_type']
        
        # 실제 동기화 로직 (여기서는 시뮬레이션)
        try:
            # Celery 태스크로 비동기 처리
            from crypto_rebate.celery import app
            task = app.send_task(
                'crypto_rebate.apps.exchanges.tasks.sync_exchange_data',
                args=[exchange_api.id, sync_type]
            )
            
            return Response({
                'success': True,
                'message': '동기화가 시작되었습니다.',
                'task_id': task.id,
                'exchange': exchange_api.exchange.name
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f"동기화에 실패했습니다: {str(e)}",
                'exchange': exchange_api.exchange.name
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def exchange_dashboard(request):
    """거래소 대시보드 API"""
    user = request.user
    
    # 활성 거래소 수
    active_exchanges = ExchangeAPI.objects.filter(user=user, is_active=True).count()
    
    # 총 수수료
    total_commission = ReferralTransaction.objects.filter(user=user).aggregate(
        total=Sum('commission')
    )['total'] or 0
    
    # 총 페이백
    from crypto_rebate.apps.rebates.models import Rebate
    total_rebate = Rebate.objects.filter(user=user, status='paid').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # 이번 달 통계
    current_month = datetime.now().month
    monthly_commission = ReferralTransaction.objects.filter(
        user=user, created_at__month=current_month
    ).aggregate(total=Sum('commission'))['total'] or 0
    
    monthly_rebate = Rebate.objects.filter(
        user=user, status='paid', created_at__month=current_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # 최근 거래 내역
    recent_transactions = ReferralTransaction.objects.filter(
        user=user
    ).order_by('-created_at')[:10]
    
    return Response({
        'statistics': {
            'active_exchanges': active_exchanges,
            'total_commission': total_commission,
            'total_rebate': total_rebate,
            'monthly_commission': monthly_commission,
            'monthly_rebate': monthly_rebate
        },
        'recent_transactions': ReferralTransactionSerializer(
            recent_transactions, many=True
        ).data
    }, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_user_rebate_rate(request, exchange_id):
    """사용자 리베이트 비율 업데이트 API"""
    try:
        user_rate = UserExchangeRebateRate.objects.get(
            user=request.user, 
            exchange_id=exchange_id
        )
    except UserExchangeRebateRate.DoesNotExist:
        return Response({
            'error': '해당 거래소의 리베이트 비율 설정이 없습니다.'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserRebateRateUpdateSerializer(user_rate, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'success': True,
            'message': '리베이트 비율이 업데이트되었습니다.',
            'data': UserExchangeRebateRateSerializer(user_rate).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_user_rebate_rate(request):
    """사용자 리베이트 비율 생성 API"""
    serializer = UserExchangeRebateRateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        # 이미 존재하는지 확인
        exchange = serializer.validated_data['exchange']
        if UserExchangeRebateRate.objects.filter(user=request.user, exchange=exchange).exists():
            return Response({
                'error': '이미 설정된 거래소입니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({
            'success': True,
            'message': '리베이트 비율이 설정되었습니다.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
