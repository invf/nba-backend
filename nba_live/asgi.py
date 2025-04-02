import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import stats.routing  # ✅ Імпорт маршрутів WebSocket

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nba_live.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(stats.routing.websocket_urlpatterns),  # ✅ Підключено WebSocket маршрути
})


