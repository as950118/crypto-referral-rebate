from django.db import models
from django.contrib.auth.models import User
from crypto_rebate.apps.exchanges.models import ReferralTransaction


class RebatePolicy(models.Model):
    POLICY_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('tiered', 'Tiered'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPE_CHOICES)
    percentage_rate = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    fixed_amount = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    minimum_amount = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    maximum_amount = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Rebate Policy"
        verbose_name_plural = "Rebate Policies"


class Rebate(models.Model):
    REBATE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rebates')
    referral_transaction = models.ForeignKey(ReferralTransaction, on_delete=models.CASCADE, related_name='rebates')
    policy = models.ForeignKey(RebatePolicy, on_delete=models.CASCADE, related_name='rebates')
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=REBATE_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.currency}"

    class Meta:
        verbose_name = "Rebate"
        verbose_name_plural = "Rebates"
        ordering = ('-created_at',)


class RebatePayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('crypto', 'Cryptocurrency'),
        ('bank', 'Bank Transfer'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
    ]

    rebate = models.OneToOneField(Rebate, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    currency = models.CharField(max_length=10)
    fee = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    net_amount = models.DecimalField(max_digits=20, decimal_places=8)
    payment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.rebate.user.username} - {self.transaction_id}"

    class Meta:
        verbose_name = "Rebate Payment"
        verbose_name_plural = "Rebate Payments"


class UserRebateSummary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rebate_summary')
    total_rebates = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    total_paid = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    pending_amount = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    last_payment_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Rebate Summary"

    class Meta:
        verbose_name = "User Rebate Summary"
        verbose_name_plural = "User Rebate Summaries"
