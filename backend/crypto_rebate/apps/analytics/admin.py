from django.contrib import admin
from .models import DailyStatistics, ExchangeStatistics, UserActivity, SystemMetrics, AuditLog


@admin.register(DailyStatistics)
class DailyStatisticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_users', 'active_users', 'total_transactions', 'total_volume', 'total_rebates', 'total_payments')
    list_filter = ('date',)
    search_fields = ('date',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date',)
    
    fieldsets = (
        ('Date', {
            'fields': ('date',)
        }),
        ('User Statistics', {
            'fields': ('total_users', 'active_users')
        }),
        ('Transaction Statistics', {
            'fields': ('total_transactions', 'total_volume')
        }),
        ('Financial Statistics', {
            'fields': ('total_rebates', 'total_payments')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ExchangeStatistics)
class ExchangeStatisticsAdmin(admin.ModelAdmin):
    list_display = ('exchange', 'date', 'total_users', 'total_transactions', 'total_volume', 'total_commissions')
    list_filter = ('exchange', 'date')
    search_fields = ('exchange__name', 'date')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date',)


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'login_count', 'transaction_count', 'rebate_amount')
    list_filter = ('date', 'user')
    search_fields = ('user__username', 'user__email', 'date')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date',)


@admin.register(SystemMetrics)
class SystemMetricsAdmin(admin.ModelAdmin):
    list_display = ('metric_type', 'name', 'value', 'unit', 'timestamp')
    list_filter = ('metric_type', 'timestamp')
    search_fields = ('name', 'metric_type')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    
    fieldsets = (
        ('Metric Information', {
            'fields': ('metric_type', 'name', 'value', 'unit')
        }),
        ('Additional Data', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'object_id', 'ip_address', 'timestamp')
    list_filter = ('action', 'model_name', 'timestamp')
    search_fields = ('user__username', 'description', 'model_name', 'object_id')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    
    fieldsets = (
        ('Action Information', {
            'fields': ('user', 'action', 'model_name', 'object_id')
        }),
        ('Details', {
            'fields': ('description', 'ip_address', 'user_agent')
        }),
        ('Timestamp', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )
