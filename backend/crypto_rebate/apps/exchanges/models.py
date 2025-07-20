from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from django.conf import settings
import json


class Exchange(models.Model):
    EXCHANGE_CHOICES = [
        ('binance', 'Binance'),
        ('upbit', 'Upbit'),
        ('bithumb', 'Bithumb'),
        ('coinbase', 'Coinbase'),
        ('kraken', 'Kraken'),
    ]

    name = models.CharField(max_length=50, choices=EXCHANGE_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    api_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = "Exchange"
        verbose_name_plural = "Exchanges"


class ExchangeAPI(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exchange_apis')
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='apis')
    api_key = models.TextField()
    api_secret = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.exchange.name} API"

    def save(self, *args, **kwargs):
        # API 키 암호화
        if not hasattr(settings, 'ENCRYPTION_KEY'):
            # 개발 환경에서는 기본 키 사용
            key = Fernet.generate_key()
        else:
            key = settings.ENCRYPTION_KEY.encode()
        
        fernet = Fernet(key)
        
        if not self.pk:  # 새로운 객체인 경우에만 암호화
            self.api_key = fernet.encrypt(self.api_key.encode()).decode()
            self.api_secret = fernet.encrypt(self.api_secret.encode()).decode()
        
        super().save(*args, **kwargs)

    def get_decrypted_api_key(self):
        key = getattr(settings, 'ENCRYPTION_KEY', Fernet.generate_key()).encode()
        fernet = Fernet(key)
        return fernet.decrypt(self.api_key.encode()).decode()

    def get_decrypted_api_secret(self):
        key = getattr(settings, 'ENCRYPTION_KEY', Fernet.generate_key()).encode()
        fernet = Fernet(key)
        return fernet.decrypt(self.api_secret.encode()).decode()

    class Meta:
        verbose_name = "Exchange API"
        verbose_name_plural = "Exchange APIs"
        unique_together = ['user', 'exchange']


class ReferralLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_links')
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='referral_links')
    referral_code = models.CharField(max_length=100, unique=True)
    referral_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.exchange.name} Referral"

    class Meta:
        verbose_name = "Referral Link"
        verbose_name_plural = "Referral Links"
        unique_together = ['user', 'exchange']


class ReferralTransaction(models.Model):
    TRANSACTION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    referral_link = models.ForeignKey(ReferralLink, on_delete=models.CASCADE, related_name='transactions')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_transactions')
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    currency = models.CharField(max_length=10)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=4)
    commission_amount = models.DecimalField(max_digits=20, decimal_places=8)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES, default='pending')
    transaction_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.referral_link.user.username} - {self.transaction_id}"

    class Meta:
        verbose_name = "Referral Transaction"
        verbose_name_plural = "Referral Transactions"
