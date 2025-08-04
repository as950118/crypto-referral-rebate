from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import RebatePolicy, Rebate, RebatePayment, UserRebateSummary
from .serializers import (
    RebatePolicySerializer, RebateSerializer, RebatePaymentSerializer,
    UserRebateSummarySerializer, RebateRequestSerializer, RebateStatsSerializer,
    RebateCalculatorSerializer
)


class RebateListView(generics.ListAPIView):
    """페이백 내역 목록 API"""
    serializer_class = RebateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Rebate.objects.filter(user=self.request.user).order_by('-created_at')


class RebateDetailView(generics.RetrieveAPIView):
    """페이백 내역 상세 API"""
    serializer_class = RebateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Rebate.objects.filter(user=self.request.user)


class RebatePaymentListView(generics.ListAPIView):
    """페이백 지급 내역 목록 API"""
    serializer_class = RebatePaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return RebatePayment.objects.filter(rebate__user=self.request.user).order_by('-created_at')


class UserRebateSummaryListView(generics.ListAPIView):
    """사용자 페이백 요약 목록 API"""
    serializer_class = UserRebateSummarySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserRebateSummary.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def request_rebate(request):
    """페이백 요청 API"""
    serializer = RebateRequestSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        exchange = serializer.validated_data['exchange']
        amount = serializer.validated_data['amount']
        payment_method = serializer.validated_data['payment_method']
        payment_address = serializer.validated_data.get('payment_address')
        
        # 사용 가능한 페이백 확인
        available_rebates = Rebate.objects.filter(
            user=user, exchange=exchange, status='pending'
        )
        
        total_available = available_rebates.aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        if amount > total_available:
            return Response({
                'error': f'요청 금액({amount})이 사용 가능한 페이백({total_available})보다 큽니다.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 페이백 지급 처리
        try:
            # 실제 지급 로직 (여기서는 시뮬레이션)
            payment = RebatePayment.objects.create(
                rebate=available_rebates.first(),  # 실제로는 여러 개를 처리해야 함
                amount=amount,
                payment_method=payment_method,
                payment_address=payment_address,
                status='processing'
            )
            
            # 페이백 상태 업데이트
            available_rebates.update(status='processing')
            
            return Response({
                'success': True,
                'message': '페이백 요청이 처리되었습니다.',
                'payment_id': payment.id,
                'amount': amount,
                'exchange': exchange.name
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'페이백 처리 중 오류가 발생했습니다: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def calculate_rebate(request):
    """페이백 계산기 API"""
    serializer = RebateCalculatorSerializer(data=request.data)
    if serializer.is_valid():
        result = serializer.calculate_rebate()
        return Response(result, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def rebate_stats(request):
    """페이백 통계 API"""
    user = request.user
    
    # 총 수익
    total_earnings = Rebate.objects.filter(
        user=user, status='paid'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # 이번 달 수익
    current_month = datetime.now().month
    monthly_earnings = Rebate.objects.filter(
        user=user, status='paid', created_at__month=current_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # 대기 중인 페이백
    pending_rebates = Rebate.objects.filter(
        user=user, status='pending'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # 지급된 페이백
    paid_rebates = Rebate.objects.filter(
        user=user, status='paid'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # 거래소별 분석
    exchange_breakdown = {}
    for rebate in Rebate.objects.filter(user=user).values('exchange__name').annotate(
        total=Sum('amount')
    ):
        exchange_breakdown[rebate['exchange__name']] = rebate['total']
    
    # 최근 페이백 내역
    recent_rebates = Rebate.objects.filter(
        user=user
    ).order_by('-created_at')[:10]
    
    return Response({
        'total_earnings': total_earnings,
        'monthly_earnings': monthly_earnings,
        'pending_rebates': pending_rebates,
        'paid_rebates': paid_rebates,
        'exchange_breakdown': exchange_breakdown,
        'recent_rebates': RebateSerializer(recent_rebates, many=True).data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def rebate_dashboard(request):
    """페이백 대시보드 API"""
    user = request.user
    
    # 통계 데이터
    stats = {
        'total_earnings': Rebate.objects.filter(
            user=user, status='paid'
        ).aggregate(total=Sum('amount'))['total'] or 0,
        'monthly_earnings': Rebate.objects.filter(
            user=user, status='paid', 
            created_at__month=datetime.now().month
        ).aggregate(total=Sum('amount'))['total'] or 0,
        'pending_rebates': Rebate.objects.filter(
            user=user, status='pending'
        ).aggregate(total=Sum('amount'))['total'] or 0,
        'total_transactions': Rebate.objects.filter(user=user).count()
    }
    
    # 거래소별 페이백
    exchange_rebates = {}
    for rebate in Rebate.objects.filter(user=user).values('exchange__name').annotate(
        total=Sum('amount')
    ):
        exchange_rebates[rebate['exchange__name']] = rebate['total']
    
    # 최근 페이백 내역
    recent_rebates = Rebate.objects.filter(
        user=user
    ).order_by('-created_at')[:5]
    
    # 페이백 상태별 개수
    status_counts = {}
    for status_choice in ['pending', 'processing', 'paid', 'failed']:
        status_counts[status_choice] = Rebate.objects.filter(
            user=user, status=status_choice
        ).count()
    
    return Response({
        'statistics': stats,
        'exchange_rebates': exchange_rebates,
        'recent_rebates': RebateSerializer(recent_rebates, many=True).data,
        'status_counts': status_counts
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def rebate_history(request):
    """페이백 히스토리 API"""
    user = request.user
    
    # 필터링 옵션
    exchange_id = request.GET.get('exchange')
    status_filter = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    queryset = Rebate.objects.filter(user=user)
    
    # 거래소 필터
    if exchange_id:
        queryset = queryset.filter(exchange_id=exchange_id)
    
    # 상태 필터
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    
    # 날짜 필터
    if start_date:
        queryset = queryset.filter(created_at__gte=start_date)
    if end_date:
        queryset = queryset.filter(created_at__lte=end_date)
    
    # 정렬
    queryset = queryset.order_by('-created_at')
    
    # 페이지네이션
    from rest_framework.pagination import PageNumberPagination
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    
    serializer = RebateSerializer(paginated_queryset, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cancel_rebate_request(request):
    """페이백 요청 취소 API"""
    rebate_id = request.data.get('rebate_id')
    
    if not rebate_id:
        return Response({
            'error': '페이백 ID를 제공해주세요.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        rebate = Rebate.objects.get(
            id=rebate_id, 
            user=request.user, 
            status='processing'
        )
        rebate.status = 'pending'
        rebate.save()
        
        return Response({
            'success': True,
            'message': '페이백 요청이 취소되었습니다.'
        }, status=status.HTTP_200_OK)
        
    except Rebate.DoesNotExist:
        return Response({
            'error': '존재하지 않는 페이백이거나 취소할 수 없는 상태입니다.'
        }, status=status.HTTP_400_BAD_REQUEST)
