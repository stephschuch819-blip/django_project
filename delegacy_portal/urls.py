"""
URL configuration for delegacy_portal project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portal/', include('portal.urls')),
    path('', include('portal.urls')),  # Also serve at root level
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Customize admin site
admin.site.site_header = "DGLegacy Portal Administration"
admin.site.site_title = "DGLegacy Admin"
admin.site.index_title = "Welcome to DGLegacy Portal Admin"
