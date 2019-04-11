import http.client
import json

PORT = 8000
SERVER = 'localhost'

# This part of the client check if when json=1 is selected, the endpoint /listSpecies works properly

conn = http.client.HTTPConnection(SERVER, PORT)
conn.request("GET", "/listSpecies?limit=10&json=1")
r1 = conn.getresponse()
print('Response received: {}\n'.format(r1.status, r1.reason))
data1 = r1.read().decode('utf-8')
response = json.loads(data1)
conn.close()
print(response)

# This part of the client check if when json=1 is selected, the endpoint /karyotype works properly

conn = http.client.HTTPConnection(SERVER, PORT)
conn.request("GET", "/karyotype?specie=human&json=1")
r1 = conn.getresponse()
print('Response received: {}\n'.format(r1.status, r1.reason))
data1 = r1.read().decode('utf-8')
response = json.loads(data1)
conn.close()
print(response)

# This part of the client check if when json=1 is selected, the endpoint /chromosomeLenght works properly

conn = http.client.HTTPConnection(SERVER, PORT)
conn.request("GET", "/chromosomeLenght?specie=human&chromo=2&json=1")
r1 = conn.getresponse()
print('Response received: {}\n'.format(r1.status, r1.reason))
data1 = r1.read().decode('utf-8')
response = json.loads(data1)
conn.close()
print(response)

# This part of the client check if when json=1 is selected, the endpoint /geneSeq works properly

conn = http.client.HTTPConnection(SERVER, PORT)
conn.request("GET", "/geneSeq?gene=FRAT1&json=1")
r1 = conn.getresponse()
print('Response received: {}\n'.format(r1.status, r1.reason))
data1 = r1.read().decode('utf-8')
response = json.loads(data1)
conn.close()
print(response)

# This part of the client check if when json=1 is selected, the endpoint /geneInfo works properly

conn = http.client.HTTPConnection(SERVER, PORT)
conn.request("GET", "/geneInfo?gene=FRAT1&json=1")
r1 = conn.getresponse()
print('Response received: {}\n'.format(r1.status, r1.reason))
data1 = r1.read().decode('utf-8')
response = json.loads(data1)
conn.close()
print(response)


# This part of the client check if when json=1 is selected, the endpoint /geneCal works properly

conn = http.client.HTTPConnection(SERVER, PORT)
conn.request("GET", "/geneCal?gene=FRAT1&json=1")
r1 = conn.getresponse()
print('Response received: {}\n'.format(r1.status, r1.reason))
data1 = r1.read().decode('utf-8')
response = json.loads(data1)
conn.close()
print(response)

# This part of the client check if when json=1 is selected, the endpoint /geneList works properly

conn = http.client.HTTPConnection(SERVER, PORT)
conn.request("GET", "/geneList?chromo=1&start=0&end=30000&json=1")
r1 = conn.getresponse()
print('Response received: {}\n'.format(r1.status, r1.reason))
data1 = r1.read().decode('utf-8')
response = json.loads(data1)
conn.close()
print(response)
