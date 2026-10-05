"""
ASGI config for mainsrc project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from customwebsocket.router import websocket_router

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainsrc.settings')

django_asgi_app = get_asgi_application()

"""

# Custom ASGI application wrapper
async def app(scope, receive, send):
    if scope['type'] == 'http':
        # Forward normal HTTP requests to Django
        await django_asgi_app(scope, receive, send)

    elif scope['type'] == 'websocket':
        # Handle WebSocket
        await websocket_app(scope, receive, send)


async def websocket_app(scope, receive, send):
    # Accept connection
    await send({
        "type": "websocket.accept"
    })

    while True:
        event = await receive()

        if event["type"] == "websocket.receive":
            # Echo back message
            msg = event.get("text", "")
            await send({
                "type": "websocket.send",
                "text": f"Echo: {msg}"
            })

        elif event["type"] == "websocket.disconnect":
            break

application = app

"""

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import websocket.urls 
import websocket.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainsrc.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocket.urls.testingwebsocket+
#             websocket.routing.websocket_urlpatterns
#         )
#     ),
# })


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
            websocket.urls.testingwebsocket+
            websocket.routing.websocket_urlpatterns
        )
})
