from django.contrib import admin
from .models import CustomUser
from app.admin import BasketAdmin

# Register your models here.



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    readonly_fields = ['password']
    inlines = (BasketAdmin,)