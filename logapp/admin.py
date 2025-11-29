from django.contrib import admin
from .models import User, Perfume, UsageLog


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ("id", "brand", "name", "capacity_ml", "created_at")
    list_filter = ("brand",)
    search_fields = ("brand", "name")


@admin.register(UsageLog)
class UsageLogAdmin(admin.ModelAdmin):
    list_display = ("id", "gender", "perfume", "user", "used_at")
    list_filter = ("gender", "perfume", "user")
    search_fields = ("user__name", "perfume__name")
