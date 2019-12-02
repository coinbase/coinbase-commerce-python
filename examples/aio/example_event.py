import os

from coinbase_commerce.aio import Client

API_KEY = os.environ.get("COINBASE_COMMERCE_API_KEY", "API_KEY")


async def main():
    async with Client(api_key=API_KEY) as client:
        # list all events
        print("#" * 100)
        ids_list = []
        async for event in client.event.list_paging_iter():
            ids_list.append(event.id)
            print("event id retrieved {}".format(event.id))

        # retrieve by id
        print("#" * 100)
        event = await client.event.retrieve(ids_list[0])
        print('{!r}'.format(event))


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(asyncio.sleep(.25))
        loop.close()
