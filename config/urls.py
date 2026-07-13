from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls',namespace='catalog')),
]


# Раздача медиа-файлов в режиме разработки (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Опционально: для статических файлов
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
