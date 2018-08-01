from mock import PropertyMock
from mock import mock
from requests import RequestException
from requests.sessions import Session

from coinbase_commerce.api_resources import Charge
from coinbase_commerce.api_resources import Checkout
from coinbase_commerce.api_resources import Event
from coinbase_commerce.client import Client
from coinbase_commerce.error import InvalidRequestError, AuthenticationError, ResourceNotFoundError, \
    RateLimitExceededError, ServiceUnavailableError, InternalServerError, ParamRequiredError, \
    ValidationError, APIError
from coinbase_commerce.response import CoinbaseResponse
from tests.base_test_case import BaseTestCase


class TestApiClient(BaseTestCase):

    def test_init(self):
        api_key, base_url, api_version = TestApiClient.mock_client_params()
        client = Client(api_key, base_url, api_version)
        self.assertEqual(client.API_VERSION, api_version)
        self.assertEqual(client.BASE_API_URI, base_url)
        self.assertIsInstance(client.session, Session)

    def test_checkout_relation(self):
        client = TestApiClient.mock_client()
        checkout = client.checkout
        checkout2 = client.checkout
        self.assertTrue(hasattr(client, 'checkout'))
        self.assertIs(checkout, Checkout)
        self.assertIs(checkout, checkout2)

    def test_charge_relation(self):
        client = TestApiClient.mock_client()
        charge = client.charge
        charge2 = client.charge
        self.assertTrue(hasattr(client, 'charge'))
        self.assertIs(charge, Charge)
        self.assertIs(charge, charge2)

    def test_event_relation(self):
        client = TestApiClient.mock_client()
        event = client.event
        event2 = client.event
        self.assertTrue(hasattr(client, 'event'))
        self.assertIs(event, Event)
        self.assertIs(event, event2)

    def test_response_class(self):
        client = TestApiClient.mock_client()
        self.stub_request('get', 'foo', {})
        resp = client._request('get', 'foo')
        self.assertTrue(isinstance(resp, CoinbaseResponse))

    def test_handle_exception(self):
        client = TestApiClient.mock_client()
        with self.assertRaises(APIError) as e:
            client._handle_request_error(Exception)
        self.assertIn("probably a configuration issue locally",
                      e.exception.args[0])

    def test_handle_request_exception(self):
        client = TestApiClient.mock_client()
        with self.assertRaises(APIError) as e:
            client._handle_request_error(RequestException())
        self.assertIn('Network error: RequestException',
                      e.exception.args[0])

    @mock.patch('requests.session', side_effect=mock.MagicMock)
    def test_invalid_request_error(self, session_mock):
        mock.MagicMock.ok = PropertyMock(return_value=False)
        mock.MagicMock.status_code = PropertyMock(return_value=400)
        client = TestApiClient.mock_client()
        with self.assertRaises(InvalidRequestError):
            client._request('get', 'foo')

    @mock.patch('requests.session', side_effect=mock.MagicMock)
    def test_authentication_error(self, session_mock):
        mock.MagicMock.ok = PropertyMock(return_value=False)
        mock.MagicMock.status_code = PropertyMock(return_value=401)
        client = TestApiClient.mock_client()
        with self.assertRaises(AuthenticationError):
            client._request('get', 'foo')

    @mock.patch('requests.session', side_effect=mock.MagicMock)
    def test_resource_not_found_error(self, session_mock):
        mock.MagicMock.ok = PropertyMock(return_value=False)
        mock.MagicMock.status_code = PropertyMock(return_value=404)
        client = TestApiClient.mock_client()
        with self.assertRaises(ResourceNotFoundError):
            client._request('get', 'foo')

    @mock.patch('requests.session', side_effect=mock.MagicMock)
    def test_rate_limit_exceeded_error(self, session_mock):
        mock.MagicMock.ok = PropertyMock(return_value=False)
        mock.MagicMock.error = {}
        mock.MagicMock.status_code = PropertyMock(return_value=429)
        client = TestApiClient.mock_client()
        with self.assertRaises(RateLimitExceededError):
            client._request('get', 'foo')

    @mock.patch('requests.session', side_effect=mock.MagicMock)
    def test_internal_server_error(self, session_mock):
        mock.MagicMock.ok = PropertyMock(return_value=False)
        mock.MagicMock.error = {}
        mock.MagicMock.status_code = PropertyMock(return_value=500)
        client = TestApiClient.mock_client()
        with self.assertRaises(InternalServerError):
            client._request('get', 'foo')

    @mock.patch('requests.session', side_effect=mock.MagicMock)
    def test_service_unavailable_error(self, session_mock):
        mock.MagicMock.ok = PropertyMock(return_value=False)
        mock.MagicMock.error = {}
        mock.MagicMock.status_code = PropertyMock(return_value=503)
        client = TestApiClient.mock_client()
        with self.assertRaises(ServiceUnavailableError):
            client._request('get', 'foo')

    @mock.patch('requests.session', side_effect=mock.MagicMock)
    def test_param_required_error(self, session_mock):
        mock.MagicMock.ok = PropertyMock(return_value=False)
        mock.MagicMock.error = PropertyMock(return_value={'type': 'param_required'})
        client = TestApiClient.mock_client()
        with self.assertRaises(ParamRequiredError):
            client._request('get', 'foo')

    @mock.patch('requests.session', side_effect=mock.MagicMock)
    def test_validation_error(self, session_mock):
        mock.MagicMock.ok = PropertyMock(return_value=False)
        mock.MagicMock.error = PropertyMock(return_value={'type': 'validation_error'})
        client = TestApiClient.mock_client()
        with self.assertRaises(ValidationError):
            client._request('get', 'foo')

    @mock.patch('requests.session', side_effect=mock.MagicMock)
    def test_valid_response_proceed(self, session_mock):
        mock.MagicMock.ok = PropertyMock(return_value=True)
        mock.MagicMock.content = '{"foo":"baz"}'
        mock.MagicMock.body = 'bar'
        mock.MagicMock.status_code = 200
        mock.MagicMock.headers = {}
        client = TestApiClient.mock_client()
        resp = client._proceed_response(mock.MagicMock)
        self.assertIsInstance(resp, CoinbaseResponse)

    @staticmethod
    def mock_client():
        api_key, base_url, api_version = TestApiClient.mock_client_params()
        return Client(api_key, base_url, api_version)

    @staticmethod
    def mock_client_params():
        api_key = 'testapikey'
        base_url = 'https://base-url.com'
        api_version = '2018-03-22'
        return api_key, base_url, api_version
