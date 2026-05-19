from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Authers learning project API",
        default_version="v1.0",
        description="This is a learning project.",
        contact=openapi.Contact(email="goodarzian.davood@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
    path(settings.ADMIN_URL, admin.site.urls),
]

admin.site.site_header = "Authors learning project API Admin"
admin.site.site_title = "API portal"
admin.site.index_title = "Welcome to authors project."