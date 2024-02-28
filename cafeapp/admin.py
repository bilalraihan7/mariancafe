from django.contrib import admin
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.

from . models import *

# admin.site.register(User)
admin.site.register(booking)
admin.site.register(foodmenu)
admin.site.register(Cart)
admin.site.register(Payment)
admin.site.register(Checkout)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'status', 'is_verified', 'view_license_button')
    list_filter = ('status', 'is_verified')
    search_fields = ('name','phone',)

    def view_license_button(self, obj):
        url = reverse('view_license', args=[obj.pk])
        return format_html('<a class="button" href="{}">View Stfaf Id Card</a>', url)

    view_license_button.short_description = ''

    def verify_license(self, request, queryset):
        for provider in queryset:
            provider.status = 'Verified'
            provider.is_verified = True
            provider.save()

    verify_license.short_description = "Verify selected providers' licenses"

    actions = [verify_license]

admin.site.register(Staff,StaffAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'is_verified', 'view_license_button')
    list_filter = ('is_verified',)
    search_fields = ('name',)

    def view_license_button(self, obj):
        url = reverse('view_license2', args=[obj.pk])
        return format_html('<a class="button" href="{}">View User Id Card</a>', url)

    view_license_button.short_description = ''

    def verify_license(self, request, queryset):
        for provider in queryset:
            provider.is_verified = True
            provider.save()

    verify_license.short_description = "Verify selected providers' licenses"

    actions = [verify_license]

admin.site.register(User,UserAdmin)



