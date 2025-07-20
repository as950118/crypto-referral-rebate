# 거래소 API 연동 기술 구현 가이드

## 📋 개요

이 문서는 주요 거래소들의 API 연동 방법과 구현 전략을 다룹니다.

## 🏢 거래소별 API 연동 가이드

### 1. Binance API 연동

#### API 엔드포인트
```python
# Binance API 설정
BINANCE_API_CONFIG = {
    'base_url': 'https://api.binance.com',
    'testnet_url': 'https://testnet.binance.vision',
    'endpoints': {
        'account': '/api/v3/account',
        'trades': '/api/v3/myTrades',
        'referral': '/sapi/v1/rebate/taxQuery',
        'commission': '/sapi/v1/rebate/taxQuery'
    }
}
```

#### 구현 예시
```python
import requests
import hmac
import hashlib
import time
from urllib.parse import urlencode

class BinanceAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = 'https://api.binance.com'
    
    def _generate_signature(self, params):
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def get_account_info(self):
        params = {
            'timestamp': int(time.time() * 1000)
        }
        params['signature'] = self._generate_signature(params)
        
        headers = {'X-MBX-APIKEY': self.api_key}
        response = requests.get(
            f"{self.base_url}/api/v3/account",
            params=params,
            headers=headers
        )
        return response.json()
    
    def get_trade_history(self, symbol=None, limit=1000):
        params = {
            'timestamp': int(time.time() * 1000),
            'limit': limit
        }
        if symbol:
            params['symbol'] = symbol
        
        params['signature'] = self._generate_signature(params)
        headers = {'X-MBX-APIKEY': self.api_key}
        
        response = requests.get(
            f"{self.base_url}/api/v3/myTrades",
            params=params,
            headers=headers
        )
        return response.json()
    
    def get_referral_info(self):
        params = {
            'timestamp': int(time.time() * 1000)
        }
        params['signature'] = self._generate_signature(params)
        headers = {'X-MBX-APIKEY': self.api_key}
        
        response = requests.get(
            f"{self.base_url}/sapi/v1/rebate/taxQuery",
            params=params,
            headers=headers
        )
        return response.json()
```

### 2. Coinbase API 연동

#### API 엔드포인트
```python
# Coinbase API 설정
COINBASE_API_CONFIG = {
    'base_url': 'https://api.coinbase.com',
    'sandbox_url': 'https://api-public.sandbox.exchange.coinbase.com',
    'endpoints': {
        'accounts': '/v2/accounts',
        'trades': '/v2/fills',
        'referral': '/v2/referral'
    }
}
```

#### 구현 예시
```python
import requests
import hmac
import hashlib
import time
import base64

class CoinbaseAPI:
    def __init__(self, api_key, api_secret, passphrase):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.base_url = 'https://api.coinbase.com'
    
    def _generate_signature(self, timestamp, method, request_path, body=''):
        message = timestamp + method + request_path + body
        signature = hmac.new(
            base64.b64decode(self.api_secret),
            message.encode('utf-8'),
            hashlib.sha256
        )
        return base64.b64encode(signature.digest()).decode('utf-8')
    
    def _make_request(self, method, endpoint, data=None):
        timestamp = str(int(time.time()))
        body = ''
        if data:
            body = str(data)
        
        signature = self._generate_signature(timestamp, method, endpoint, body)
        
        headers = {
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
        
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=headers, data=body)
        return response.json()
    
    def get_accounts(self):
        return self._make_request('GET', '/v2/accounts')
    
    def get_trades(self, product_id=None):
        endpoint = '/v2/fills'
        if product_id:
            endpoint += f'?product_id={product_id}'
        return self._make_request('GET', endpoint)
```

### 3. KuCoin API 연동

#### API 엔드포인트
```python
# KuCoin API 설정
KUCOIN_API_CONFIG = {
    'base_url': 'https://api.kucoin.com',
    'sandbox_url': 'https://openapi-sandbox.kucoin.com',
    'endpoints': {
        'accounts': '/api/v1/accounts',
        'trades': '/api/v1/fills',
        'referral': '/api/v1/referral'
    }
}
```

#### 구현 예시
```python
import requests
import hmac
import hashlib
import base64
import time
import json

class KuCoinAPI:
    def __init__(self, api_key, api_secret, passphrase):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
        self.base_url = 'https://api.kucoin.com'
    
    def _generate_signature(self, timestamp, method, endpoint, data=''):
        str_to_sign = f"{timestamp}{method}{endpoint}{data}"
        signature = base64.b64encode(
            hmac.new(
                self.api_secret.encode('utf-8'),
                str_to_sign.encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode('utf-8')
        return signature
    
    def _make_request(self, method, endpoint, data=None):
        timestamp = str(int(time.time() * 1000))
        body = ''
        if data:
            body = json.dumps(data)
        
        signature = self._generate_signature(timestamp, method, endpoint, body)
        passphrase = base64.b64encode(
            hmac.new(
                self.api_secret.encode('utf-8'),
                self.passphrase.encode('utf-8'),
                hashlib.sha256
            ).digest()
        ).decode('utf-8')
        
        headers = {
            'KC-API-SIGN': signature,
            'KC-API-TIMESTAMP': timestamp,
            'KC-API-KEY': self.api_key,
            'KC-API-PASSPHRASE': passphrase,
            'KC-API-KEY-VERSION': '2',
            'Content-Type': 'application/json'
        }
        
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=headers, data=body)
        return response.json()
    
    def get_accounts(self):
        return self._make_request('GET', '/api/v1/accounts')
    
    def get_trades(self, symbol=None):
        endpoint = '/api/v1/fills'
        if symbol:
            endpoint += f'?symbol={symbol}'
        return self._make_request('GET', endpoint)
```

## 🔧 Django 모델 확장

### 거래소별 설정 모델
```python
# crypto_rebate/apps/exchanges/models.py에 추가

class ExchangeAPIConfig(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    api_base_url = models.URLField()
    api_version = models.CharField(max_length=10)
    rate_limit_per_minute = models.IntegerField(default=60)
    is_sandbox = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Exchange API Config"
        verbose_name_plural = "Exchange API Configs"

class APICallLog(models.Model):
    exchange_api = models.ForeignKey(ExchangeAPI, on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=200)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    response_time = models.FloatField()  # milliseconds
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "API Call Log"
        verbose_name_plural = "API Call Logs"
```

## 🚀 Celery 태스크 구현

### 거래소 데이터 수집 태스크
```python
# crypto_rebate/apps/exchanges/tasks.py

from celery import shared_task
from .models import ExchangeAPI, ReferralTransaction
from .services import BinanceAPI, CoinbaseAPI, KuCoinAPI
import logging

logger = logging.getLogger(__name__)

@shared_task
def collect_binance_trades(exchange_api_id):
    """Binance 거래 내역 수집"""
    try:
        exchange_api = ExchangeAPI.objects.get(id=exchange_api_id)
        
        # API 클라이언트 생성
        api_client = BinanceAPI(
            exchange_api.get_decrypted_api_key(),
            exchange_api.get_decrypted_api_secret()
        )
        
        # 거래 내역 가져오기
        trades = api_client.get_trade_history()
        
        # 데이터베이스에 저장
        for trade in trades:
            ReferralTransaction.objects.get_or_create(
                transaction_id=trade['id'],
                defaults={
                    'referral_link': exchange_api.user.referral_links.filter(
                        exchange__name='binance'
                    ).first(),
                    'amount': trade['qty'],
                    'currency': trade['quoteAsset'],
                    'commission_amount': trade['commission'],
                    'status': 'completed',
                    'transaction_date': trade['time']
                }
            )
        
        logger.info(f"Collected {len(trades)} trades from Binance")
        
    except Exception as e:
        logger.error(f"Error collecting Binance trades: {e}")
        raise

@shared_task
def collect_coinbase_trades(exchange_api_id):
    """Coinbase 거래 내역 수집"""
    try:
        exchange_api = ExchangeAPI.objects.get(id=exchange_api_id)
        
        api_client = CoinbaseAPI(
            exchange_api.get_decrypted_api_key(),
            exchange_api.get_decrypted_api_secret(),
            exchange_api.passphrase
        )
        
        trades = api_client.get_trades()
        
        for trade in trades:
            ReferralTransaction.objects.get_or_create(
                transaction_id=trade['trade_id'],
                defaults={
                    'referral_link': exchange_api.user.referral_links.filter(
                        exchange__name='coinbase'
                    ).first(),
                    'amount': trade['size'],
                    'currency': trade['product_id'],
                    'commission_amount': trade['fee'],
                    'status': 'completed',
                    'transaction_date': trade['created_at']
                }
            )
        
        logger.info(f"Collected {len(trades)} trades from Coinbase")
        
    except Exception as e:
        logger.error(f"Error collecting Coinbase trades: {e}")
        raise

@shared_task
def collect_kucoin_trades(exchange_api_id):
    """KuCoin 거래 내역 수집"""
    try:
        exchange_api = ExchangeAPI.objects.get(id=exchange_api_id)
        
        api_client = KuCoinAPI(
            exchange_api.get_decrypted_api_key(),
            exchange_api.get_decrypted_api_secret(),
            exchange_api.passphrase
        )
        
        trades = api_client.get_trades()
        
        for trade in trades:
            ReferralTransaction.objects.get_or_create(
                transaction_id=trade['tradeId'],
                defaults={
                    'referral_link': exchange_api.user.referral_links.filter(
                        exchange__name='kucoin'
                    ).first(),
                    'amount': trade['size'],
                    'currency': trade['symbol'],
                    'commission_amount': trade['fee'],
                    'status': 'completed',
                    'transaction_date': trade['createdAt']
                }
            )
        
        logger.info(f"Collected {len(trades)} trades from KuCoin")
        
    except Exception as e:
        logger.error(f"Error collecting KuCoin trades: {e}")
        raise
```

## 📊 페이백 계산 서비스

### 페이백 계산 로직
```python
# crypto_rebate/apps/rebates/services.py

from decimal import Decimal
from .models import RebatePolicy, Rebate
from ..exchanges.models import ReferralTransaction

class RebateCalculator:
    def __init__(self, user):
        self.user = user
    
    def calculate_rebate(self, transaction):
        """거래에 대한 페이백 계산"""
        # 사용자의 페이백 정책 가져오기
        policy = self.get_user_policy()
        
        # 거래소별 페이백 비율 적용
        exchange_rate = self.get_exchange_rate(transaction.referral_link.exchange.name)
        
        # 기본 페이백 계산
        base_rebate = transaction.commission_amount * exchange_rate
        
        # 정책에 따른 조정
        if policy.policy_type == 'percentage':
            final_rebate = base_rebate * policy.percentage_rate
        elif policy.policy_type == 'fixed':
            final_rebate = min(base_rebate, policy.fixed_amount)
        else:  # tiered
            final_rebate = self.calculate_tiered_rebate(base_rebate, policy)
        
        # 최소/최대 금액 제한
        if policy.minimum_amount and final_rebate < policy.minimum_amount:
            final_rebate = Decimal('0')
        
        if policy.maximum_amount and final_rebate > policy.maximum_amount:
            final_rebate = policy.maximum_amount
        
        return final_rebate
    
    def get_exchange_rate(self, exchange_name):
        """거래소별 페이백 비율"""
        rates = {
            'binance': Decimal('0.28'),
            'coinbase': Decimal('0.25'),
            'kucoin': Decimal('0.32'),
            'bybit': Decimal('0.28'),
            'okx': Decimal('0.25'),
            'kraken': Decimal('0.22')
        }
        return rates.get(exchange_name, Decimal('0.20'))
    
    def calculate_tiered_rebate(self, base_amount, policy):
        """단계별 페이백 계산"""
        # 사용자 등급에 따른 배율 적용
        user_tier = self.get_user_tier()
        tier_multipliers = {
            'bronze': Decimal('1.0'),
            'silver': Decimal('1.1'),
            'gold': Decimal('1.2'),
            'platinum': Decimal('1.3')
        }
        
        multiplier = tier_multipliers.get(user_tier, Decimal('1.0'))
        return base_amount * multiplier
    
    def get_user_tier(self):
        """사용자 등급 계산"""
        total_volume = self.user.referral_links.aggregate(
            total=models.Sum('transactions__amount')
        )['total'] or Decimal('0')
        
        if total_volume >= Decimal('10000'):
            return 'platinum'
        elif total_volume >= Decimal('5000'):
            return 'gold'
        elif total_volume >= Decimal('1000'):
            return 'silver'
        else:
            return 'bronze'
```

## 🔒 보안 설정

### API 키 암호화
```python
# crypto_rebate/apps/exchanges/utils.py

from cryptography.fernet import Fernet
from django.conf import settings
import base64

def encrypt_api_key(api_key):
    """API 키 암호화"""
    key = getattr(settings, 'ENCRYPTION_KEY', Fernet.generate_key())
    fernet = Fernet(key)
    return fernet.encrypt(api_key.encode()).decode()

def decrypt_api_key(encrypted_key):
    """API 키 복호화"""
    key = getattr(settings, 'ENCRYPTION_KEY', Fernet.generate_key())
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_key.encode()).decode()
```

## 📈 모니터링 및 알림

### API 상태 모니터링
```python
# crypto_rebate/apps/analytics/services.py

from .models import SystemMetrics
import time

class APIMonitor:
    @staticmethod
    def log_api_call(exchange_name, endpoint, response_time, status_code):
        """API 호출 로그 기록"""
        SystemMetrics.objects.create(
            metric_type='performance',
            name=f'{exchange_name}_api_response_time',
            value=response_time,
            unit='ms',
            metadata={
                'endpoint': endpoint,
                'status_code': status_code,
                'exchange': exchange_name
            }
        )
    
    @staticmethod
    def check_api_health():
        """API 상태 체크"""
        exchanges = ['binance', 'coinbase', 'kucoin']
        for exchange in exchanges:
            # API 상태 확인 로직
            pass
```

---

**작성일**: 2024년 7월 20일  
**버전**: 1.0  
**작성자**: AI Assistant 