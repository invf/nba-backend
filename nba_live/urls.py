from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("stats.urls")),  # Переконайся, що цей рядок є
]
