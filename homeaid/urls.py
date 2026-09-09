from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth & Users endpoints
    path('api/auth/', include('users.urls')),
    path('api/users/', include('users.urls')),

    # Core app endpoints
    path('api/services/', include('services.urls')),
    path('api/providers/', include('providers.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/sos/', include('sos.urls')),
    path('api/messages/', include('chat.urls')),

    # Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]