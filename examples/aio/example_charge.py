"""
name	            string	Required	Charge name
description	        string	Required	More detailed description of the
charge
pricing_type	    string	Required	Charge pricing type: no_price or
fixed_price
local_price	         money	Optional	Price in local fiat currency
metadata	          hash	Optional	Developer defined key value pairs
redirect_url	    string	Optional	Redirect URL
"""
import os

from coinbase_commerce.aio import Client

API_KEY = os.environ.get("COINBASE_COMMERCE_API_KEY", "API_KEY")


async def main():
    # initialize client
    async with Client(api_key=API_KEY) as client:
        # charge info
        charge_info = {
            "name": "The Sovereign Individual",
            "description": "Mastering the Transition to the Information Age",
            "local_price": {
                "amount": "100.00",
                "currency": "USD"
            },
            "pricing_type": "fixed_price"

        }
        charge = await client.charge.create(**charge_info)
        saved_charge_id = charge.id

        print("Created charge {!r}".format(charge))
        print("#" * 100)

        charge_list = await client.charge.list(limit=1)
        print("charges list")
        print(charge_list.data)
        print("#" * 100)

        print("auto charge list iteration")
        async for charge in client.charge.list_paging_iter(limit=3):
            print("{!r}".format(charge))
        print("#" * 100)

        retrieved_charge = await client.charge.retrieve(
            entity_id=saved_charge_id
        )
        print("retrieved charge {!r}".format(retrieved_charge))


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(asyncio.sleep(.25))
        loop.close()
