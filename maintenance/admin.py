from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import MaintenanceSettings


@admin.register(MaintenanceSettings)
class MaintenanceSettingsAdmin(ModelAdmin):

    compressed_fields = True
    warn_unsaved_form = True
    list_fullwidth    = True

    readonly_fields = ("last_updated", "current_status")

    fieldsets = (
        (
            _("Current Status"),
            {
                "classes": ["tab"],
                "fields": ("current_status", "last_updated"),
            },
        ),
        (
            _("Maintenance Controls"),
            {
                "classes": ["tab"],
                "fields": (
                    "site_under_maintenance",
                    "forum_under_maintenance",
                    "maintenance_until",
                ),
            },
        ),
    )

    list_display = (
        "panel_label",
        "site_badge",
        "forum_badge",
        "maintenance_until",
        "last_updated",
    )

    def has_add_permission(self, request):
        return not MaintenanceSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj, _ = MaintenanceSettings.objects.get_or_create(pk=1)
        return HttpResponseRedirect(
            reverse("admin:maintenance_maintenancesettings_change", args=[obj.pk])
        )

    @display(description=_("Status"))
    def current_status(self, obj):
        rows = [
            ("Entire Website", obj.site_under_maintenance),
            ("Forum Section",  obj.forum_under_maintenance),
        ]
        html = '<div style="display:flex;flex-direction:column;gap:8px;padding:4px 0;">'
        for label, active in rows:
            if active:
                bg, border, color, text = "#fff1f2", "#fecdd3", "#be123c", "Under Maintenance"
            else:
                bg, border, color, text = "#f0fdf4", "#bbf7d0", "#15803d", "Operational"
            html += (
                f'<div style="display:inline-flex;align-items:center;gap:12px;'
                f'background:{bg};border:1px solid {border};color:{color};'
                f'padding:8px 16px;border-radius:8px;font-size:13px;width:fit-content;">'
                f'<span style="font-weight:400;color:#6b7280;min-width:110px;">{label}</span>'
                f'<span style="width:1px;height:12px;background:{border};"></span>'
                f'<span style="font-weight:600;">{text}</span></div>'
            )
        html += '</div>'
        return format_html(html)

    @display(description=_("Panel"))
    def panel_label(self, obj):
        return format_html(
            '<span style="font-size:13px;font-weight:600;color:#111827;">Maintenance Control</span>'
        )

    @display(description=_("Entire Website"), ordering="site_under_maintenance")
    def site_badge(self, obj):
        return self._badge(obj.site_under_maintenance)

    @display(description=_("Forum Section"), ordering="forum_under_maintenance")
    def forum_badge(self, obj):
        return self._badge(obj.forum_under_maintenance)

    @staticmethod
    def _badge(is_active):
        if is_active:
            return format_html(
                '<span style="background:#fff1f2;color:#be123c;border:1px solid #fecdd3;'
                'padding:3px 12px;border-radius:6px;font-size:12px;font-weight:600;'
                'display:inline-block;">Maintenance</span>'
            )
        return format_html(
            '<span style="background:#f0fdf4;color:#15803d;border:1px solid #bbf7d0;'
            'padding:3px 12px;border-radius:6px;font-size:12px;font-weight:600;'
            'display:inline-block;">Operational</span>'
        )