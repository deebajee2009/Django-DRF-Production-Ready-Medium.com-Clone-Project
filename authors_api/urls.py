from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from dj_rest_auth.views import PasswordResetConfirmView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from core_apps.users.views import CustomUserDetailsView


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
    path("api/v1/auth/user", CustomUserDetailsView.as_view(), name="user_details"),
    path("api/v1/auth", include("dj_rest_auth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/v1/auth/password/reset/confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("api/v1/profiles/", include("core_apps.profiles.urls")),
    path("api/v1/article/", include("core_apps.articles.urls")),
    path("api/v1/ratings/", include("core_apps.ratings.urls")),
    path("api/v1/bookmarks/", include("core_apps.bookmarks.urls")),
    path("api/v1/responses/", include("core_apps.responses.urls")),
]

admin.site.site_header = "Authors learning project API Admin"
admin.site.site_title = "API portal"
admin.site.index_title = "Welcome to authors project."
