from django.contrib import admin
from .models import Exchange, UserExchangeRebateRate, ExchangeAPI, ReferralLink, ReferralTransaction


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_base_rebate_rate_percentage', 'min_withdrawal', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_base_rebate_rate_percentage(self, obj):
        return f"{obj.rebate_rate_percentage:.2f}%"
    get_base_rebate_rate_percentage.short_description = '기본 리베이트 비율'
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'logo', 'website', 'api_documentation')
        }),
        ('리베이트 설정', {
            'fields': ('base_rebate_rate', 'min_withdrawal')
        }),
        ('지원 정보', {
            'fields': ('supported_countries', 'features')
        }),
        ('상태', {
            'fields': ('is_active',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserExchangeRebateRate)
class UserExchangeRebateRateAdmin(admin.ModelAdmin):
    list_display = ['user', 'exchange', 'get_custom_rebate_rate_percentage', 'get_effective_rebate_rate_percentage', 'is_active', 'created_at']
    list_filter = ['is_active', 'exchange', 'created_at']
    search_fields = ['user__username', 'exchange__name']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_custom_rebate_rate_percentage(self, obj):
        return f"{obj.custom_rebate_rate_percentage:.2f}%"
    get_custom_rebate_rate_percentage.short_description = '커스텀 리베이트 비율'
    
    def get_effective_rebate_rate_percentage(self, obj):
        return f"{obj.effective_rebate_rate_percentage:.2f}%"
    get_effective_rebate_rate_percentage.short_description = '실제 리베이트 비율'
    
    fieldsets = (
        ('사용자 정보', {
            'fields': ('user', 'exchange')
        }),
        ('리베이트 설정', {
            'fields': ('custom_rebate_rate', 'is_active')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ExchangeAPI)
class ExchangeAPIAdmin(admin.ModelAdmin):
    list_display = ['user', 'exchange', 'is_active', 'last_sync', 'created_at']
    list_filter = ['is_active', 'exchange', 'created_at']
    search_fields = ['user__username', 'exchange__name']
    readonly_fields = ['created_at', 'updated_at', 'get_effective_rebate_rate_percentage']
    
    def get_effective_rebate_rate_percentage(self, obj):
        return f"{obj.effective_rebate_rate_percentage:.2f}%"
    get_effective_rebate_rate_percentage.short_description = '실제 리베이트 비율'
    
    fieldsets = (
        ('사용자 정보', {
            'fields': ('user', 'exchange')
        }),
        ('API 정보', {
            'fields': ('api_key', 'api_secret', 'passphrase')
        }),
        ('상태', {
            'fields': ('is_active', 'last_sync')
        }),
        ('리베이트 정보', {
            'fields': ('get_effective_rebate_rate_percentage',),
            'classes': ('collapse',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ReferralLink)
class ReferralLinkAdmin(admin.ModelAdmin):
    list_display = ['user', 'exchange', 'referral_code', 'clicks', 'conversions', 'total_commission', 'is_active', 'created_at']
    list_filter = ['is_active', 'exchange', 'created_at']
    search_fields = ['user__username', 'exchange__name', 'referral_code']
    readonly_fields = ['created_at', 'updated_at', 'get_effective_rebate_rate_percentage']
    
    def get_effective_rebate_rate_percentage(self, obj):
        return f"{obj.effective_rebate_rate_percentage:.2f}%"
    get_effective_rebate_rate_percentage.short_description = '실제 리베이트 비율'
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('user', 'exchange', 'referral_code', 'referral_link')
        }),
        ('통계', {
            'fields': ('clicks', 'conversions', 'total_commission')
        }),
        ('상태', {
            'fields': ('is_active',)
        }),
        ('리베이트 정보', {
            'fields': ('get_effective_rebate_rate_percentage',),
            'classes': ('collapse',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ReferralTransaction)
class ReferralTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'exchange', 'transaction_id', 'amount', 'commission', 'status', 'created_at']
    list_filter = ['status', 'exchange', 'created_at']
    search_fields = ['user__username', 'exchange__name', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at', 'get_effective_rebate_rate_percentage', 'get_calculated_rebate_amount']
    
    def get_effective_rebate_rate_percentage(self, obj):
        return f"{obj.effective_rebate_rate_percentage:.2f}%"
    get_effective_rebate_rate_percentage.short_description = '실제 리베이트 비율'
    
    def get_calculated_rebate_amount(self, obj):
        return f"${obj.calculated_rebate_amount:.2f}"
    get_calculated_rebate_amount.short_description = '계산된 리베이트 금액'
    
    fieldsets = (
        ('거래 정보', {
            'fields': ('user', 'exchange', 'referral_link', 'transaction_id')
        }),
        ('금액 정보', {
            'fields': ('amount', 'commission', 'commission_rate')
        }),
        ('상태', {
            'fields': ('status',)
        }),
        ('리베이트 정보', {
            'fields': ('get_effective_rebate_rate_percentage', 'get_calculated_rebate_amount'),
            'classes': ('collapse',)
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
