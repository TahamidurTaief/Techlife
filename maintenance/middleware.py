from .models import MaintenanceSettings

FORUM_PREFIXES = ("/forum/",)

EXEMPT_PREFIXES = (
    "/admin/",
    "/static/",
    "/media/",
    "/api-auth/",
    "/__reload__/",
    "/ckeditor/",
)


def _starts_with_any(path, prefixes):
    return any(path.startswith(p) for p in prefixes)


class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if _starts_with_any(path, EXEMPT_PREFIXES):
            request.maintenance_section = None
            return self.get_response(request)

        config = MaintenanceSettings.get()

        section = None
        if config.site_under_maintenance:
            section = "site"
        elif config.forum_under_maintenance and _starts_with_any(path, FORUM_PREFIXES):
            section = "forum"

        request.maintenance_section = section
        request.maintenance_config  = config if section else None

        return self.get_response(request)