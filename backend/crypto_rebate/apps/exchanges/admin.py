from django.contrib import admin
from .models import Exchange, ExchangeAPI, ReferralLink, ReferralTransaction


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'api_url', 'is_active', 'created_at')
    list_filter = ('is_active', 'name')
    search_fields = ('name', 'display_name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)


@admin.register(ExchangeAPI)
class ExchangeAPIAdmin(admin.ModelAdmin):
    list_display = ('user', 'exchange', 'is_active', 'created_at')
    list_filter = ('is_active', 'exchange', 'created_at')
    search_fields = ('user__username', 'user__email', 'exchange__name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'exchange')
        }),
        ('API Configuration', {
            'fields': ('api_key', 'api_secret', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ReferralLink)
class ReferralLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'exchange', 'referral_code', 'is_active', 'created_at')
    list_filter = ('is_active', 'exchange', 'created_at')
    search_fields = ('user__username', 'exchange__name', 'referral_code')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(ReferralTransaction)
class ReferralTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'referral_link', 'referred_user', 'amount', 'currency', 'commission_amount', 'status', 'transaction_date')
    list_filter = ('status', 'currency', 'transaction_date', 'created_at')
    search_fields = ('transaction_id', 'referral_link__user__username', 'referred_user__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-transaction_date',)
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('transaction_id', 'referral_link', 'referred_user', 'status')
        }),
        ('Financial Details', {
            'fields': ('amount', 'currency', 'commission_rate', 'commission_amount')
        }),
        ('Timestamps', {
            'fields': ('transaction_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
