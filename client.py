import http.client
import json

# -- API information + method + port
HOSTNAME = "localhost"
METHOD = "GET"
PORT = 8000


def convert_dict(self, path):
    dictionary = dict()
    keyvalue = path.split('?')[1]
    keyvalue = keyvalue.split(' ')[0]
    list = keyvalue.split('&')
    for keyandvalue in list:
        key = keyandvalue.split('=')[0]
        value = keyandvalue.split('=')[1]
        dictionary[key] = value
    return dictionary


# -- Here we can define special headers if needed
headers = {'User-Agent': 'http-client'}

# -- Connect to the server
# -- NOTICE it is an HTTPS connection!
# -- If we do not specify the port, the standard one
# -- will be used
conn = http.client.HTTPSConnection(HOSTNAME)

ENDPOINT = '/listSpecies?limit=&json=1'

# -- Send the request. No body (None)
# -- Use the defined headers
conn.request(METHOD,ENDPOINT, None, headers)

# -- Wait for the server's response
r1 = conn.getresponse()

# -- Print the status
print()
print("Response received: ", end='')
print(r1.status, r1.reason)

# -- Read the response's body and close
# -- the connection
text_json = r1.read().decode("utf-8")


parameters = self.convert_dict(self.path)
limit = parameters['limit']

# -- Optionally you can print the
# -- received json file for testing
# print(text_json)

# -- Generate the object from the json file
listSpecies = json.loads(text_json)

list_of_species = list1['species']

# -- Get the data
count = 0
List = []

for one in list_of_species:
    specie = one['name']
    List.append(specie)
    count = count + 1

    if int(count) == int(limit):
        break

Dict = {}
Dict['List_of_species'] = List

contents = json.dumps(Dict)
print(contents)