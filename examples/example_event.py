from coinbase_commerce.client import Client

API_KEY = "API_KEY"
client = Client(api_key=API_KEY)

ids_list = []

# list all events
print("#" * 100)
for event in client.event.list_paging_iter():
    ids_list.append(event.id)
    print("event id retrieved {}".format(event.id))

# retrieve by id
print("#" * 100)
event = client.event.retrieve(ids_list[0])
print('{!r}'.format(event))
