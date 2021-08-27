from django.conf.urls import url
from django.contrib import admin
from django.urls import (
    path,
    include,
)

urlpatterns = [
    path("api/", include("apps.dish.urls")),
    path("admin/", admin.site.urls),

    #
    url(r"^silk/", include("silk.urls", namespace="silk"))
]
