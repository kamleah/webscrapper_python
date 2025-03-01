from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Scrapper App API",
        default_version="v1",
        description="Scrapper API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="example@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    # url='https://2285-106-205-184-39.ngrok-free.app/',
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(
        "scrapper-api/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("scrap/", include("scrap.urls")),
    path("account/", include("account.urls")),
]
