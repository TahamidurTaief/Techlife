from django.contrib import admin
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import TemplateView
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from blog_post.models import BlogPost

from django.views.static import serve
from django.urls import re_path

class PostSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    protocol = "https"

    def items(self):
        return BlogPost.objects.filter(status="published").order_by("-created_at")

    def lastmod(self, obj):
        return getattr(obj, "updated_at", obj.created_at)

    def location(self, obj):
        return f"/details/{obj.slug}/"


sitemaps = {"posts": PostSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
    # path("__reload__/", include("django_browser_reload.urls")),  # Temporarily commented - install django-browser-reload
    path("", include("blog_post.urls")),
    path("account/", include("accounts.urls")),
    path("contact/", include("contact.urls")),
    path("forum/", include("forum.urls")),
    
    path('api-auth/', include('rest_framework.urls')),
    path('api/blog/', include('blog_post.api_urls')),

    path("__reload__/", include("django_browser_reload.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# This works in both DEBUG=True and DEBUG=False
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]