import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HackBios.settings')
asgi_application = get_asgi_application()


from channels.routing import URLRouter , ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from base import routing as base_routing

application = ProtocolTypeRouter(
    {
        "http" : asgi_application , 
        "websocket" : 
            AuthMiddlewareStack(
                URLRouter(
                    [
                        *base_routing.websocket_urlpatterns ,  
                    ]
                )
            
        )
    }
)