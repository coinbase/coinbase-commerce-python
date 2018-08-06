[![CircleCI](https://circleci.com/gh/coinbase/coinbase-commerce-python/tree/master.svg?style=svg)](https://circleci.com/gh/coinbase/coinbase-commerce-python/tree/master)

# coinbase-commerce-python
Coinbase Commerce Python

# Table of contents

<!--ts-->
   * [Python Versions](#python-version)
   * [Third Party Libraries and Dependencies](#third-party-libraries-and-dependencies)
   * [Documentation](#documentation)
   * [Installation](#installation)
   * [Usage](#usage)
      * [Checkouts](#checkouts)
      * [Charges](#charges)
      * [Events](#events)
   * [Validating webhook signatures](#validating-webhook-signatures)
   * [Testing and Contributing](#testing-and-contributing)
<!--te-->

## Python Version
Python 2.7+ and 3.4+ are supported and tested.

## Third Party Libraries and Dependencies

The following libraries will be installed when you install the client library:
* [requests](https://github.com/requests/requests)

## Documentation

For more details visit [Coinbase API docs](https://commerce.coinbase.com/docs/api/).

To start using library, you need to register on [Commerce SignUp](https://commerce.coinbase.com/signup).
And get your ``API_KEY`` from user settings.

Next create a ``Client`` object for interacting with the API:
```python
from coinbase_commerce.client import Client

API_KEY = "API KEY"
client = Client(api_key=API_KEY)
```

``Client`` contains links to an every Python Class representations of the API resources
``Checkout, Charge, Event``

You can call ``list, list_paging_iter, create, retrieve, modify`` methods from an API resource classes

```python
client.charge.create
client.checkout.list_paging_iter 
client.event.list
client.charge.retrieve
client.checkout.modify
```
as well as ``save, delete, refresh`` methods from API resource class instances.
```python
checkout = client.checkout.retrieve(<id>)
checkout.refresh()
checkout.save()
checkout.delete()
```

Each API method returns an ``APIObject`` (a subclass of ``dict``) representing the JSON response from the API, all of the models are dumpable with JSON.\
Also when the response data is parsed into Python objects, the appropriate ``APIObject`` subclasses will be used automatically.
All subclasses of ``APIResource`` class support ``refresh`` method. This will update their attributes and all nested data by making a fresh ``GET`` request to the relevant API endpoint.

Client support Common API Errors and Warnings handling.
All errors occuring during interaction with the API will be raised as exceptions.


| Error                    | Status Code |
|--------------------------|-------------|
| APIError                 |      *      |   
| InvalidRequestError      |     400     |   
| ParamRequiredError       |     400     |  
| ValidationError          |     400     |  
| AuthenticationError      |     401     |  
| ResourceNotFoundError    |     404     |
| RateLimitExceededError   |     429     |
| InternalServerError      |     500     |
| ServiceUnavailableError  |     503     |

## Installation

Install with ``pip``:

    pip install --upgrade coinbase-commerce

or with ``easy_install``:

    easy_install --upgrade coinbase-commerce


## Usage
```python
from coinbase_commerce.client import Client

client = Client(api_key=API_KEY)
```
## Checkouts 
[Checkouts API docs](https://commerce.coinbase.com/docs/api/#checkouts)
### Retrieve
```python
checkout = client.checkout.retrieve(<checkout_id>)
```
### Create
```python
checkout_info = {
    "name": 'The Sovereign Individual',
    "description": 'Mastering the Transition to the Information Age',
    "pricing_type": 'fixed_price',
    "local_price": {
        "amount": "100.00",
        "currency": "USD"
    },
    "requested_info": ["name", "email"]
}
checkout = client.checkout.create(**checkout_info)

# or

checkout = client.checkout.create(name='The Sovereign Individual',
                                  description='Mastering the Transition to the Information Age',
                                  pricing_type='fixed_price',
                                  local_price={
                                          "amount": "100.00",
                                          "currency": "USD"
                                          },
                                  requested_info=["name", "email"])                            
```
### Update
```python
checkout = client.checkout.retrieve(<checkout_id>)
checkout.name = 'new name'
checkout.save()

# or

checkout = client.checkout.modify('<checkout_id>',
                                  name='new name')
```
### Delete
```python
checkout.delete()
```
### List
```python
checkouts = client.checkout.list()
```
### Paging list iterations
```python
for checkout in client.checkout.list_paging_iter():
    print("{!r}".format(checkout))

```
## Charges
[Charges API docs](https://commerce.coinbase.com/docs/api/#charges)
### Retrieve
```python
charge = client.charge.retrieve(<charge_id>)
```
### Create
```python
charge_info = {
    "name": "The Sovereign Individual",
    "description": "Mastering the Transition to the Information Age",
    "local_price": {
        "amount": "100.00",
        "currency": "USD"
    },
    "pricing_type": "fixed_price"

}
charge = client.charge.create(**charge_info)

# or

charge = client.charge.create(name='The Sovereign Individual',
                              description='Mastering the Transition to the Information Age',
                              pricing_type='fixed_price',
                              local_price={
                                  "amount": "100.00",
                                  "currency": "USD"
                              })
```
### List
```python
checkouts = client.charge.list()
```
### Paging list iterations
```python
for charge in client.charge.list_paging_iter():
    print("{!r}".format(charge))
```
## Events
[Events API Docs](https://commerce.coinbase.com/docs/api/#events)
### Retrieve
```python
event = client.event.retrieve(<event_id>)
```
### List
```python
events = client.event.list()
```
### Paging list iterations
```python
for event in client.event.list_paging_iter():
    print("{!r}".format(event))
```

## Validating webhook signatures
You could verify webhook signatures using our library.
To perform the verification you'll need to provide the event data, a webhook signature from request header, and the endpoint’s secret.
In case of invalid request signature or request payload, you will receive appropriate error message.
```python
WEBHOOK_SECRET = 'your_webhook_secret'

# using Flask
@app.route('/webhooks', methods=['POST'])
def webhooks():
    # event payload
    request_data = request.data.decode('utf-8')
    # webhook signature
    request_sig = request.headers.get('X-CC-Webhook-Signature', None)

    try:
        # signature verification and event object construction
        event = Webhook.construct_event(request_data, request_sig, WEBHOOK_SECRET)
    except (WebhookInvalidPayload, SignatureVerificationError) as e:
        return str(e), 400

    print("Received event: id={id}, type={type}".format(id=event.id, type=event.type))
    return 'success', 200
```

### Testing and Contributing
Any and all contributions are welcome! The process is simple: fork this repo, make your changes, run the test suite, and submit a pull request. Tests are run via nosetest. To run the tests, clone the repository and then:

#### Install the requirements
```
pip install -r requirements.txt
```

####  Run the tests for your current version of Python
Use tox to run the test suite against multiple versions of Python. You can install tox with pip or easy_install:
```
pip install tox
easy_install tox
```
Tox requires the appropriate Python interpreters to run the tests in different environments. We recommend using pyenv for this. Once you've installed the appropriate interpreters, running the tests in every environment is simple:
```
tox
```
