"""
# name	                      string	Required	Checkout name
# description	              string	Required	More detailed description
# pricing_type	              string	Required	Checkout pricing type: no_price or fixed_price
# local_price	               money	Optional	Price in local fiat currency
# requested_info	           array	Optional	Information to collect from the customer: email, name
"""
import os

from coinbase_commerce import Client

API_KEY = os.environ.get("COINBASE_COMMERCE_API_KEY", "API_KEY")

# initialize client
client = Client(api_key=API_KEY)

checkout_info = {
    "name": "The Sovereign Individual",
    "description": "Mastering the Transition to the Information Age",
    "pricing_type": 'fixed_price',
    "local_price": {
        "amount": "1.00",
        "currency": "USD"
    },
    "requested_info": ["name", "email"]
}

print("#" * 100)
# simple create
checkout_item = client.checkout.create(**checkout_info)
print("{!r}".format(checkout_item))

print("#" * 100)
# create in list
for item in range(40):
    checkout_info['name'] = 'item {}'.format(item)
    ch = client.checkout.create(**checkout_info)
    print("checkout {} created".format(ch.id))

count = 0
ids_list = []
print("#" * 100)
# modify all checkouts
for checkout in client.checkout.list_paging_iter():
    count += 1
    ids_list.append(checkout.id)
    checkout.description = "new description {}".format(count)
    checkout.save()
    print("checkout {} updated".format(checkout.id))

# modify all by ids
print("#" * 100)
for checkout_id in ids_list:
    ch = client.checkout.modify(checkout_id, name='new name')
    print("checkout {} updated".format(ch.id))

# retrieve by id
print("#" * 100)
retrieved_checkout = client.checkout.retrieve(ids_list[0])
print("retrieved {!r}".format(retrieved_checkout))

# delete all checkouts [DANGER]
checkouts = []
for checkout in client.checkout.list_paging_iter():
    checkouts.append(checkout)

for checkout in checkouts:
    print("deleting {}".format(checkout.id))
    checkout.delete()
