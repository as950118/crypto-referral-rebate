from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone_number', 'get_is_verified')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__is_verified')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'profile__phone_number')

    def get_phone_number(self, obj):
        return obj.profile.phone_number if hasattr(obj, 'profile') else '-'
    get_phone_number.short_description = 'Phone Number'

    def get_is_verified(self, obj):
        return obj.profile.is_verified if hasattr(obj, 'profile') else False
    get_is_verified.short_description = 'Verified'
    get_is_verified.boolean = True


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
