"""
aiohttp server example to test webhooks
You may need tunnels to localhost webhook development tool and debugging tool.
f.e. you could try ngrok
"""
import os

from aiohttp import web

from coinbase_commerce.error import (
    SignatureVerificationError,
    WebhookInvalidPayload,
)
from coinbase_commerce.webhook import Webhook


WEBHOOK_SECRET = os.environ.get(
    "COINBASE_COMMERCE_WEBHOOK_SECRET",
    "your_webhook_secret"
)

app = web.Application()
app['wh_secret'] = WEBHOOK_SECRET
routes = web.RouteTableDef()


@routes.post('/webhooks')
async def webhooks(request):
    request_data = await request.text()
    request_sig = request.headers.get('X-CC-Webhook-Signature', None)

    try:
        event = Webhook.construct_event(
            payload=request_data,
            sig_header=request_sig,
            secret=request.app['wh_secret']
        )
    except (WebhookInvalidPayload, SignatureVerificationError) as e:
        raise web.HTTPBadRequest(body=str(e))

    print("Received event: id={id}, type={type}".format(
        id=event.id,
        type=event.type
    ))
    return web.Response(body='success')


app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=int(os.environ.get('PORT', 5000)))
