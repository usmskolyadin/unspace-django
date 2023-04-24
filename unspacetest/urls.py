from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from utopies.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('utopies/', include('utopies.urls')),
    path('itutopies/', include('itutopies.urls')),
    path('regauth/', include('regauth.urls')),
    path('accounts/', include('allauth.urls')),
    path('dev/', include('dev.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns