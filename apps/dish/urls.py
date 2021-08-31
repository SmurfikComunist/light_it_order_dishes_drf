from django.conf.urls import url
from django.urls import (
    path,
    include,
)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import (
    routers,
    permissions,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="Order dishes API",
        default_version="v1",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = routers.DefaultRouter()
router.register(r"ingredients", views.IngredientViewSet)
router.register(r"dishes", views.DishViewSet)
router.register(r"orders", views.OrderViewSet)

urlpatterns = (
    path("", include(router.urls)),

    # JWT
    path(
        "token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),

    # API Documentation
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
)
