from django.contrib import admin
from .models import contact_or_support, FooterSettings
from unfold.admin import ModelAdmin

@admin.register(contact_or_support)
class ContactOrSupportAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "user", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("name", "email", "phone", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    fieldsets = (
        ("User Info", {
            "fields": ("user", "name", "email", "phone")
        }),
        ("Message Details", {
            "fields": ("message",)
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )



from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import FooterSettings

@admin.register(FooterSettings)
class FooterSettingsAdmin(ModelAdmin):
    # Organizes the dashboard into logical sections
    fieldsets = (
        ("Brand & Identity", {
            "fields": ("logo", "description"),
        }),
        ("Contact Information", {
            "fields": ("email", "phone", "address"),
        }),
        ("Social Media Presence", {
            "fields": ("facebook_url", "twitter_url", "linkedin_url", "whatsapp_number"),
            "description": "Enter the full URLs for social platforms and phone number for WhatsApp.",
        }),
        ("Development Credits", {
            "fields": ("developer_company_name", "developer_company_url"),
        }),
    )

    # Singleton Pattern: Prevents creating more than one settings entry
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True

    # Prevents deleting the configuration accidentally
    def has_delete_permission(self, request, obj=None):
        return False

    # Optional: Display a summary in the list view
    list_display = ("__str__", "email", "phone", "developer_company_name")