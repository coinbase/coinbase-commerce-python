from coinbase_commerce.api_resources.event import Event
from coinbase_commerce.error import SignatureVerificationError
from coinbase_commerce.error import WebhookInvalidPayload
from coinbase_commerce.webhook import Webhook
from coinbase_commerce.webhook import WebhookSignature
from tests.base_test_case import BaseTestCase

PAYLOAD_STR = '{"id":1,' \
              '"scheduled_for":"2017-01-31T20:50:02Z",' \
              '"attempt_number":1,' \
              '"event":{' \
              '"id":"24934862-d980-46cb-9402-43c81b0cdba6",' \
              '"type":"charge:created",' \
              '"api_version":"2018-03-22",' \
              '"created_at":"2017-01-31T20:49:02Z",' \
              '"data":{' \
              '"code":"66BEOV2A",' \
              '"name":"The Sovereign Individual",' \
              '"description":"Mastering the Transition to the Information Age",' \
              '"hosted_url":"https://commerce.coinbase.com/charges/66BEOV2A",' \
              '"created_at":"2017-01-31T20:49:02Z",' \
              '"expires_at":"2017-01-31T21:04:02Z",' \
              '"timeline":[{"time":"2017-01-31T20:49:02Z","status":"NEW"}],' \
              '"metadata":{},"pricing_type":"no_price","payments":[],' \
              '"addresses":{' \
              '"bitcoin":"0000000000000000000000000000000000",' \
              '"ethereum":"0x0000000000000000000000000000000000000000",' \
              '"litecoin":"3000000000000000000000000000000000",' \
              '"bitcoincash":"bitcoincash:000000000000000000000000000000000000000000"}' \
              '}}}'
SIG_HEADER = '8be7742c7d372f08a6a3224edadf18a22b65fa9e28f3f2de97376cdaa092590d'
SECRET = '30291a20-0bd1-4267-9b0f-e6e7b123c0bf'


class TestWebhook(BaseTestCase):

    def test_success_signature_verification(self):
        result = WebhookSignature.verify_sig_header(PAYLOAD_STR, SIG_HEADER, SECRET)
        self.assertTrue(result)

    def test_fail_signature_verification(self):
        invalid_sig_header = SIG_HEADER.replace('3', '1')
        with self.assertRaises(SignatureVerificationError) as context:
            WebhookSignature.verify_sig_header(PAYLOAD_STR, invalid_sig_header, SECRET)
        self.assertTrue("No signatures found matching the expected signature " \
                        "{0} for payload {1}".format(invalid_sig_header, PAYLOAD_STR) in str(context.exception))

    def test_invalid_payload_not_json(self):
        invalid_payload_str = 'invalid payload'
        with self.assertRaises(WebhookInvalidPayload) as context:
            Webhook.construct_event(invalid_payload_str, SIG_HEADER, SECRET)
        self.assertTrue('Invalid payload provided' in str(context.exception))

    def test_invalid_payload_no_event(self):
        payload_without_event = '{"id":1,"scheduled_for":"2017-01-31T20:50:02Z","attempt_number":1}'
        with self.assertRaises(WebhookInvalidPayload) as context:
            Webhook.construct_event(payload_without_event, SIG_HEADER, SECRET)
        self.assertTrue('Invalid payload provided' in str(context.exception))

    def test_event_construct(self):
        event = Webhook.construct_event(PAYLOAD_STR, SIG_HEADER, SECRET)
        self.assertIsInstance(event, Event)
        self.assertEqual(event.id, '24934862-d980-46cb-9402-43c81b0cdba6')
