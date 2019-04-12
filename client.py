import http.client
import json

# Define the server and the server's port
PORT = 8000
SERVER = 'localhost'

# This part of the client check if when json=1 is selected, the endpoint /listSpecies works properly

# Establishing connection to the Server
conn = http.client.HTTPConnection(SERVER, PORT)
conn.request("GET", "/listSpecies?limit=10&json=1")

# Get the response
r1 = conn.getresponse()

# Check The status of the response
print('Response received: {}\n'.format(r1.status, r1.reason))

# Decoding the response
data1 = r1.read().decode('utf-8')

# Closing the connection
conn.close()

# Creating a dictionary from the response received
response = json.loads(data1)

# Print JSON text
print(response)

# This part of the client check if when json=1 is selected, the endpoint /karyotype works properly

# Establishing connection to the Server
conn = http.client.HTTPConnection(SERVER, PORT)
conn.request("GET", "/karyotype?specie=human&json=1")

# Get the response
r1 = conn.getresponse()

# Check The status of the response
print('Response received: {}\n'.format(r1.status, r1.reason))

# Decoding the response
data1 = r1.read().decode('utf-8')

# Closing the connection
conn.close()

# Creating a dictionary from the response received
response = json.loads(data1)

# Print JSON text
print(response)

# This part of the client check if when json=1 is selected, the endpoint /chromosomeLenght works properly

# Establishing connection to the Server
conn = http.client.HTTPConnection(SERVER, PORT)
conn.request("GET", "/chromosomeLength?specie=mouse&chromo=10&json=1")

# Get the response
r1 = conn.getresponse()

# Check The status of the response
print('Response received: {}\n'.format(r1.status, r1.reason))

# Decoding the response
data1 = r1.read().decode('utf-8')

# Closing the connection
conn.close()

# Creating a dictionary from the response received
response = json.loads(data1)

# Print JSON text
print(response)

# This part of the client check if when json=1 is selected, the endpoint /geneSeq works properly

# Establishing connection to the Server
conn = http.client.HTTPConnection(SERVER, PORT)
conn.request("GET", "/geneSeq?gene=FRAT1&json=1")

# Get the response
r1 = conn.getresponse()

# Check The status of the response
print('Response received: {}\n'.format(r1.status, r1.reason))

# Decoding the response
data1 = r1.read().decode('utf-8')

# Closing the connection
conn.close()

# Creating a dictionary from the response received
response = json.loads(data1)

# Print JSON text
print(response)

# This part of the client check if when json=1 is selected, the endpoint /geneInfo works properly

# Establishing connection to the Server
conn = http.client.HTTPConnection(SERVER, PORT)
conn.request("GET", "/geneInfo?gene=FRAT1&json=1")

# Get the response
r1 = conn.getresponse()

# Check The status of the response
print('Response received: {}\n'.format(r1.status, r1.reason))

# Decoding the response
data1 = r1.read().decode('utf-8')

# Closing the connection
conn.close()

# Creating a dictionary from the response received
response = json.loads(data1)

# Print JSON text
print(response)


# This part of the client check if when json=1 is selected, the endpoint /geneCal works properly

# Establishing connection to the Server
conn = http.client.HTTPConnection(SERVER, PORT)
conn.request("GET", "/geneCal?gene=FRAT1&json=1")

# Get the response
r1 = conn.getresponse()

# Check The status of the response
print('Response received: {}\n'.format(r1.status, r1.reason))

# Decoding the response
data1 = r1.read().decode('utf-8')

# Closing the connection
conn.close()

# Creating a dictionary from the response received
response = json.loads(data1)

# Print JSON text
print(response)

# This part of the client check if when json=1 is selected, the endpoint /geneList works properly

# Establishing connection to the Server
conn = http.client.HTTPConnection(SERVER, PORT)
conn.request("GET", "/geneList?chromo=1&start=0&end=30000&json=1")

# Get the response
r1 = conn.getresponse()

# Check The status of the response
print('Response received: {}\n'.format(r1.status, r1.reason))

# Decoding the response
data1 = r1.read().decode('utf-8')

# Closing the connection
conn.close()

# Creating a dictionary from the response received
response = json.loads(data1)

# Print JSON text
print(response)
