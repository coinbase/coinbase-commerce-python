"""
# name	                      string	Required	Checkout name
# description	              string	Required	More detailed description
# pricing_type	              string	Required	Checkout pricing type:
no_price or fixed_price
# local_price	               money	Optional	Price in local fiat
currency
# requested_info	           array	Optional	Information to collect
from the customer: email, name
"""
import os

from coinbase_commerce.aio import Client

API_KEY = os.environ.get("COINBASE_COMMERCE_API_KEY", "API_KEY")


async def main():
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

    # initialize client
    async with Client(api_key=API_KEY) as client:
        print("#" * 100)
        # simple create
        checkout_item = await client.checkout.create(**checkout_info)
        print("{!r}".format(checkout_item))

        print("#" * 100)
        # create in list
        checkouts = []
        for item in range(40):
            checkout_info['name'] = 'item {}'.format(item)
            ch = await client.checkout.create(**checkout_info)
            checkouts.append(ch)
            print("checkout {} created".format(ch.id))

        print("#" * 100)
        # modify all checkouts
        for count, checkout in enumerate(checkouts, 1):
            checkout.description = "new description {}".format(count)
            await checkout.save()
            print("checkout {} updated".format(checkout.id))

        # modify all by ids
        print("#" * 100)
        for checkout in checkouts:
            ch = await client.checkout.modify(checkout.id, name='new name')
            print("checkout {} updated".format(ch.id))

        # retrieve by id
        print("#" * 100)
        retrieved_checkout = await client.checkout.retrieve(checkouts[0].id)
        print("retrieved {!r}".format(retrieved_checkout))

        # delete created checkouts
        for checkout in checkouts:
            print("deleting {}".format(checkout.id))
            await checkout.delete()


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(asyncio.sleep(.25))
        loop.close()
