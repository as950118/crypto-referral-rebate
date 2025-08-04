from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from cryptography.fernet import Fernet
from django.conf import settings
import json

User = get_user_model()


class Exchange(models.Model):
    """거래소 정보"""
    name = models.CharField(max_length=100, unique=True)
    logo = models.URLField(blank=True, default='')
    website = models.URLField(default='https://example.com')
    api_documentation = models.URLField(blank=True, default='')
    base_rebate_rate = models.DecimalField(
        max_digits=5, decimal_places=4,  # 0.0000 ~ 1.0000 (0% ~ 100%)
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="기본 리베이트 비율 (0.45 = 45%)",
        default=0.40  # 40% 기본값
    )
    min_withdrawal = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    supported_countries = models.JSONField(default=list, blank=True)
    features = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exchanges'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def rebate_rate_percentage(self):
        """리베이트 비율을 퍼센트로 반환"""
        return float(self.base_rebate_rate) * 100


class UserExchangeRebateRate(models.Model):
    """사용자별 거래소 리베이트 비율"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exchange_rebate_rates')
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='user_rebate_rates')
    custom_rebate_rate = models.DecimalField(
        max_digits=5, decimal_places=4,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="사용자별 커스텀 리베이트 비율",
        default=0.40  # 40% 기본값
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_exchange_rebate_rates'
        unique_together = ['user', 'exchange']
        ordering = ['user', 'exchange']

    def __str__(self):
        return f"{self.user.username} - {self.exchange.name}: {self.custom_rebate_rate_percentage}%"

    @property
    def custom_rebate_rate_percentage(self):
        """커스텀 리베이트 비율을 퍼센트로 반환"""
        return float(self.custom_rebate_rate) * 100

    @property
    def effective_rebate_rate(self):
        """실제 적용되는 리베이트 비율"""
        return self.custom_rebate_rate if self.is_active else self.exchange.base_rebate_rate

    @property
    def effective_rebate_rate_percentage(self):
        """실제 적용되는 리베이트 비율을 퍼센트로 반환"""
        return float(self.effective_rebate_rate) * 100


class ExchangeAPI(models.Model):
    """거래소 API 연동 정보"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exchange_apis')
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='apis')
    api_key = models.TextField()
    api_secret = models.TextField()
    passphrase = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_sync = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exchange_apis'
        unique_together = ['user', 'exchange']
        ordering = ['user', 'exchange']

    def __str__(self):
        return f"{self.user.username} - {self.exchange.name} API"

    def save(self, *args, **kwargs):
        """API 키 암호화 저장"""
        if not self.pk:  # 새로 생성되는 경우에만 암호화
            fernet = Fernet(settings.ENCRYPTION_KEY.encode())
            self.api_key = fernet.encrypt(self.api_key.encode()).decode()
            self.api_secret = fernet.encrypt(self.api_secret.encode()).decode()
            if self.passphrase:
                self.passphrase = fernet.encrypt(self.passphrase.encode()).decode()
        super().save(*args, **kwargs)

    def get_api_key(self):
        """암호화된 API 키 복호화"""
        fernet = Fernet(settings.ENCRYPTION_KEY.encode())
        return fernet.decrypt(self.api_key.encode()).decode()

    def get_api_secret(self):
        """암호화된 API 시크릿 복호화"""
        fernet = Fernet(settings.ENCRYPTION_KEY.encode())
        return fernet.decrypt(self.api_secret.encode()).decode()

    def get_passphrase(self):
        """암호화된 패스프레이즈 복호화"""
        if not self.passphrase:
            return None
        fernet = Fernet(settings.ENCRYPTION_KEY.encode())
        return fernet.decrypt(self.passphrase.encode()).decode()

    @property
    def effective_rebate_rate(self):
        """실제 적용되는 리베이트 비율"""
        try:
            user_rate = UserExchangeRebateRate.objects.get(
                user=self.user, 
                exchange=self.exchange,
                is_active=True
            )
            return user_rate.effective_rebate_rate
        except UserExchangeRebateRate.DoesNotExist:
            return self.exchange.base_rebate_rate

    @property
    def effective_rebate_rate_percentage(self):
        """실제 적용되는 리베이트 비율을 퍼센트로 반환"""
        return float(self.effective_rebate_rate) * 100


class ReferralLink(models.Model):
    """레퍼럴 링크"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_links')
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='referral_links')
    referral_code = models.CharField(max_length=100, default='')
    referral_link = models.URLField(default='https://example.com')
    clicks = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    total_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'referral_links'
        unique_together = ['user', 'exchange']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.exchange.name} Referral"

    @property
    def effective_rebate_rate(self):
        """실제 적용되는 리베이트 비율"""
        try:
            user_rate = UserExchangeRebateRate.objects.get(
                user=self.user, 
                exchange=self.exchange,
                is_active=True
            )
            return user_rate.effective_rebate_rate
        except UserExchangeRebateRate.DoesNotExist:
            return self.exchange.base_rebate_rate

    @property
    def effective_rebate_rate_percentage(self):
        """실제 적용되는 리베이트 비율을 퍼센트로 반환"""
        return float(self.effective_rebate_rate) * 100


class ReferralTransaction(models.Model):
    """레퍼럴 거래 내역"""
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('confirmed', '확인됨'),
        ('paid', '지급됨'),
        ('failed', '실패'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_transactions')
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='referral_transactions')
    referral_link = models.ForeignKey(ReferralLink, on_delete=models.CASCADE, related_name='transactions')
    transaction_id = models.CharField(max_length=255, unique=True, default='')
    amount = models.DecimalField(max_digits=15, decimal_places=8, default=0)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'referral_transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.exchange.name} - {self.transaction_id}"

    @property
    def effective_rebate_rate(self):
        """실제 적용되는 리베이트 비율"""
        try:
            user_rate = UserExchangeRebateRate.objects.get(
                user=self.user, 
                exchange=self.exchange,
                is_active=True
            )
            return user_rate.effective_rebate_rate
        except UserExchangeRebateRate.DoesNotExist:
            return self.exchange.base_rebate_rate

    @property
    def calculated_rebate_amount(self):
        """계산된 리베이트 금액"""
        return self.commission * self.effective_rebate_rate
