import os

from flask import Flask, request

from coinbase_commerce.error import WebhookInvalidPayload, SignatureVerificationError
from coinbase_commerce.webhook import Webhook

"""
Flask server example to test webhooks
You may need tunnels to localhost webhook development tool and debugging tool.
f.e. you could try ngrok
"""
WEBHOOK_SECRET = 'your_webhook_secret'

app = Flask(__name__)


@app.route('/webhooks', methods=['POST'])
def webhooks():
    request_data = request.data.decode('utf-8')
    request_sig = request.headers.get('X-CC-Webhook-Signature', None)

    try:
        event = Webhook.construct_event(request_data, request_sig, WEBHOOK_SECRET)
    except (WebhookInvalidPayload, SignatureVerificationError) as e:
        return str(e), 400

    print("Received event: id={id}, type={type}".format(id=event.id, type=event.type))
    return 'success', 200


if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 5000)))
