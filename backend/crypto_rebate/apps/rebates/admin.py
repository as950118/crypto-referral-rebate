from django.contrib import admin
from .models import RebatePolicy, Rebate, RebatePayment, UserRebateSummary


@admin.register(RebatePolicy)
class RebatePolicyAdmin(admin.ModelAdmin):
    list_display = ('name', 'policy_type', 'percentage_rate', 'fixed_amount', 'is_active', 'created_at')
    list_filter = ('policy_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)
    
    fieldsets = (
        ('Policy Information', {
            'fields': ('name', 'description', 'policy_type', 'is_active')
        }),
        ('Rate Configuration', {
            'fields': ('percentage_rate', 'fixed_amount', 'minimum_amount', 'maximum_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Rebate)
class RebateAdmin(admin.ModelAdmin):
    list_display = ('user', 'referral_transaction', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'currency', 'created_at', 'payment_date')
    search_fields = ('user__username', 'user__email', 'referral_transaction__transaction_id')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Rebate Information', {
            'fields': ('user', 'referral_transaction', 'policy', 'status')
        }),
        ('Financial Details', {
            'fields': ('amount', 'currency', 'payment_date', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RebatePayment)
class RebatePaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'rebate', 'payment_method', 'amount', 'currency', 'net_amount', 'payment_date')
    list_filter = ('payment_method', 'currency', 'payment_date')
    search_fields = ('transaction_id', 'rebate__user__username')
    readonly_fields = ('payment_date',)
    ordering = ('-payment_date',)
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('rebate', 'payment_method', 'transaction_id')
        }),
        ('Financial Details', {
            'fields': ('amount', 'currency', 'fee', 'net_amount', 'notes')
        }),
        ('Timestamps', {
            'fields': ('payment_date',),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserRebateSummary)
class UserRebateSummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_rebates', 'total_paid', 'pending_amount', 'last_payment_date', 'updated_at')
    list_filter = ('last_payment_date', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('updated_at',)
    ordering = ('-updated_at',)
