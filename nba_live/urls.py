from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def index(request):
    return HttpResponse("👋 Hello from Django backend on Render!")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('stats.urls')),

    # ✅ додай цей маршрут на головну "/"
    path('', index),
]
