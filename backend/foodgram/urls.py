from django.conf import settings
#from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

#handler404 = 'backend.recipes.views.page_not_found'
#handler500 = 'backend.recipes.views.server_error'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('backend.api.urls')),
    path('auth/', include('backend.users.urls')),
    path('', include('backend.recipes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
