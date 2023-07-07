from django.contrib import admin
from .models import User,Revenue
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class CustomUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Hash the password if it is set or updated
        if 'password' in form.changed_data:
            obj.set_password(obj.password)

        # Save the user
        super().save_model(request, obj, form, change)

admin.site.register(User, CustomUserAdmin)

class RevenueAdmin(admin.ModelAdmin):
    list_display = ['__str__', '__markedpaid__', 'fee_amount', 'submission_date']
admin.site.register(Revenue, RevenueAdmin)