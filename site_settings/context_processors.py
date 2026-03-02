from .models import SiteSettings

def site_settings(request):
    settings = SiteSettings.get_settings()
    return {
        'GOOGLE_ANALYTICS_ID': settings.google_analytics_id,
        'SITE_TITLE': settings.site_title,
        'META_DESCRIPTION': settings.meta_description,
    }