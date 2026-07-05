from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('documents/', RedirectView.as_view(pattern_name='documentos:lista', permanent=False)),
    path('documentacion/', RedirectView.as_view(pattern_name='documentos:lista', permanent=False)),
    path('documentos/', include('documents.urls')),
]

# Servir archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)