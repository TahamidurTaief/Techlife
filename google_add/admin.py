
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Advertisement

@admin.register(Advertisement)
class AdvertisementAdmin(ModelAdmin):
    list_display = ['order', 'title', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']
    ordering = ['order']
    search_fields = ['title']
    
    fieldsets = (
        ("Ad Information", {
            "fields": ("title", "order", "is_active"),
        }),
        ("Ad Code", {
            "fields": ("ad_code",),
        }),
    )