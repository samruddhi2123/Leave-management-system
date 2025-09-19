from django.contrib import admin
from .models import Leave

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ("student", "start_date", "end_date", "reason", "status", "applied_at")
    list_filter = ("status", "start_date", "end_date")

# Register your models here.
