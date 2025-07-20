from django.db import models
from django.contrib.auth.models import User
from crypto_rebate.apps.exchanges.models import Exchange


class DailyStatistics(models.Model):
    date = models.DateField(unique=True)
    total_users = models.IntegerField(default=0)
    active_users = models.IntegerField(default=0)
    total_transactions = models.IntegerField(default=0)
    total_volume = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    total_rebates = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    total_payments = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Statistics for {self.date}"

    class Meta:
        verbose_name = "Daily Statistics"
        verbose_name_plural = "Daily Statistics"
        ordering = ('-date',)


class ExchangeStatistics(models.Model):
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='statistics')
    date = models.DateField()
    total_users = models.IntegerField(default=0)
    total_transactions = models.IntegerField(default=0)
    total_volume = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    total_commissions = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.exchange.name} - {self.date}"

    class Meta:
        verbose_name = "Exchange Statistics"
        verbose_name_plural = "Exchange Statistics"
        unique_together = ['exchange', 'date']
        ordering = ('-date',)


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    date = models.DateField()
    login_count = models.IntegerField(default=0)
    transaction_count = models.IntegerField(default=0)
    rebate_amount = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    class Meta:
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"
        unique_together = ['user', 'date']
        ordering = ('-date',)


class SystemMetrics(models.Model):
    METRIC_TYPE_CHOICES = [
        ('performance', 'Performance'),
        ('error', 'Error'),
        ('security', 'Security'),
        ('business', 'Business'),
    ]

    metric_type = models.CharField(max_length=20, choices=METRIC_TYPE_CHOICES)
    name = models.CharField(max_length=100)
    value = models.FloatField()
    unit = models.CharField(max_length=20, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.metric_type} - {self.name}: {self.value}"

    class Meta:
        verbose_name = "System Metric"
        verbose_name_plural = "System Metrics"
        ordering = ('-timestamp',)


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('api_call', 'API Call'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs', null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'System'} - {self.action} - {self.timestamp}"

    class Meta:
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
        ordering = ('-timestamp',)
