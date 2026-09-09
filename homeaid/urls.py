from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    # Authentication
    path(
        "api/auth/",
        include("users.urls")
    ),

    # Services
    path(
        "api/services/",
        include("services.urls")
    ),

    # Swagger / OpenAPI
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema"
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui"
    ),
]