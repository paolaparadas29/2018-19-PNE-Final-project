import socketserver
import termcolor
import http.server
import http.client
import json
from Seq import Seq

# Define the server's port, the hostname and method
HOSTNAME = "rest.ensembl.org"
METHOD = "GET"
PORT = 8000


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler

class TestHandler(http.server.BaseHTTPRequestHandler):

    # A function which takes the path and create a dictionary with all the parameters needed to answer the request
    def convert_dict(self, path):

        # Creating a dictionary with the different parameters contain in the path
        Dict = dict()
        keyvalue = path.split('?')[1]
        keyvalue = keyvalue.split(' ')[0]
        listt = keyvalue.split('&')

        # Loop for iterating over the different values in the list 'listt' to fill the dictionary
        for keyandvalue in listt:
            name_parameter = keyandvalue.split('=')[0]
            value_parameter = keyandvalue.split('=')[1]
            Dict[name_parameter] = value_parameter

        return Dict

    # A method is called whenever the client invokes the GET method in the HTTP protocol request
    def do_GET(self):

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # Selecting type of resource that must be used to create the response to the client

        # Whenever the resource '/' is selected, this part of the program is executed
        if self.path == '/':
            # Assigning a value to the variable 'jsonvalue'
            # which then will be used to decide what content type should be sent in the headers
            jsonvalue = 0

            # Assigning to the variable contents the name of the 'index.html' file
            contents = 'index.html'

            # Open the file and read the content in 'index.html'
            with open(contents, 'r') as a:
                contents = a.read()
                a.close()

        # Whenever the resource '/listSpecies' is selected, this part of the program is executed
        elif '/listSpecies' in self.path:

            # Condition to differentiate when a limit of species is requested and when it is not
            if 'limit' in self.path:

                # This try-catch is created to deal with Value or Type errors
                try:
                    # Create a variable of class Dict which contains the parameters needed to find
                    # a proper response to the client
                    keyandvalue = self.convert_dict(self.path)

                    # Using the key 'limit' in the Dictionary 'keyandvalue' to assign that value to the variable 'limit'
                    limit = keyandvalue['limit']

                    # Define the endpoint and the headers
                    ENDPOINT = "/info/species?content-type=application/json"
                    headers = {'User-Agent': 'http-client'}

                    # Establishing connection to the Server
                    conn = http.client.HTTPConnection(HOSTNAME)
                    conn.request(METHOD, ENDPOINT, None, headers)

                    # Get the response
                    r1 = conn.getresponse()

                    # Check The status of the response
                    print()
                    print("Response received: ", end='')
                    print(r1.status, r1.reason)

                    # Decoding the response
                    text_json = r1.read().decode("utf-8")

                    # Closing the connection
                    conn.close()

                    # Creating a dictionary from the response received
                    data1 = json.loads(text_json)

                    # Creating a list with the species
                    species = data1['species']

                # This part of the code is executed whenever a type error arises
                except TypeError:

                    # Define the endpoint and the headers
                    ENDPOINT = "/info/species?content-type=application/json"
                    headers = {'User-Agent': 'http-client'}

                    # Establishing connection to the Server
                    conn = http.client.HTTPConnection(HOSTNAME)
                    conn.request(METHOD, ENDPOINT, None, headers)

                    # Get the response
                    r1 = conn.getresponse()

                    # Check The status of the response
                    print()
                    print("Response received: ", end='')
                    print(r1.status, r1.reason)

                    # Decoding the response
                    text_json = r1.read().decode("utf-8")

                    # Closing the connection
                    conn.close()

                    # Creating a list from the response received
                    data1 = json.loads(text_json)

                    # Creating a list with the species
                    species = data1['species']

                    # Assigning the value of the number of all the species to the variable limit to deal with this error
                    limit = len(species)

                # This try-catch deals with value errors
                try:
                    int(limit)
                except ValueError:
                    limit = len(species)

            # Condition executed when the limit is not requested
            else:
                # Define the endpoint and the headers
                ENDPOINT = "/info/species?content-type=application/json"
                headers = {'User-Agent': 'http-client'}

                # Establishing connection to the Server
                conn = http.client.HTTPConnection(HOSTNAME)
                conn.request(METHOD, ENDPOINT, None, headers)

                # Get the response
                r1 = conn.getresponse()

                # Check The status of the response
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)

                # Decoding the response
                text_json = r1.read().decode("utf-8")

                # Closing the connection
                conn.close()

                # Creating a dictionary from the response received
                data1 = json.loads(text_json)

                # Creating a list with the species
                species = data1['species']

                # Assigning the value of the number of all the species to the variable limit to deal with this error
                limit = len(species)

            # Define a counter and an list which after going over the loop will contain the names of the species
            count = 0
            List = []

            # Loop for going over the list of species and taking their names until the limit has been reached
            for one in species:
                specie = one['name']
                List.append(specie)
                count = count + 1

                if int(count) == int(limit):
                    break

            # Creating a dictionary which contains the name of the species
            Dict = {}
            Dict['Species'] = List

            # Loop to decide whether to send a json or a html file depending if the parameter json=1 was selected or not
            if 'json=1' in self.path:

                # Assigning a value to the variable 'jsonvalue'
                # which then will be used to decide what content type should be sent in the headers
                jsonvalue = 1

                # Converting in text json the dictionary 'Dict' and assigning it to the variable 'contents'
                contents = json.dumps(Dict)

            else:
                # Assigning a value to the variable 'jsonvalue'
                # which then will be used to decide what content type should be sent in the headers
                jsonvalue = 0

                # Creating a html text with the name of the species and assigning it to the variable 'contents'
                contents = """
                            <html>
                  <body style="background-color: green;">
                    <h1>List of all species</h1>
                            <ul>"""
                count = 0
                for one in species:
                    contents = contents + '<li>' + one['name'] + '</li>'
                    count = count + 1

                    if int(count) == int(limit):
                        break
                contents = contents + """
                            </ul>
                            </body>
                            </html>
                            """

        # Whenever the resource '/listSpecies' is selected, this part of the program is executed
        elif '/karyotype' in self.path:

            # Create a variable of class Dict which contains the parameters needed to find
            # a proper response to the client
            keyandvalue = self.convert_dict(self.path)

            # This try-catch deals with key errors
            try:
                # Using the key 'specie' in the Dictionary 'keyandvalue' to assign that value to the variable 'name'
                name = keyandvalue['specie']

                # Define the endpoint and the headers
                ENDPOINT = "/info/assembly/" + name + "?"
                headers = {'Content-Type': 'application/json'}

                # Establishing connection to the Server
                conn = http.client.HTTPConnection(HOSTNAME)
                conn.request(METHOD, ENDPOINT, None, headers)

                # Get the response
                r1 = conn.getresponse()

                # Check The status of the response
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)

                # Decoding the response
                text_json = r1.read().decode("utf-8")

                # Closing the connection
                conn.close()

                # Creating a dictionary from the response received
                response = json.loads(text_json)

                # Using the key 'karyotype' to assign that value to the variable 'karyotype'
                karyotype = response['karyotype']

                # Creating a dictionary which contains the karyotype of the specie
                Dict = {}
                Dict['karyotype'] = response['karyotype']

                # Loop to decide whether to send a json or a html file depending
                # if the parameter json=1 was selected or not
                if 'json=1' in self.path:

                    # Assigning a value to the variable 'jsonvalue'
                    # which then will be used to decide what content type should be sent in the headers
                    jsonvalue = 1

                    # Converting in text json the dictionary 'Dict' and assigning it to the variable 'contents'
                    contents = json.dumps(Dict)

                else:
                    # Assigning a value to the variable 'jsonvalue'
                    # which then will be used to decide what content type should be sent in the headers
                    jsonvalue = 0

                    # Creating a html text with the karyotype of the specie and assigning it to the variable 'contents'
                    contents = """
                                <html>
                      <body style="background-color: lightblue;">
                        <h1>Karyotype</h1>
                                <ul>"""
                    for one in karyotype:
                        contents = contents + '<li>' + one + '</li>'

                    contents = contents + """
                                </ul>
                                </body>
                                </html>
                                """
            except KeyError:
                # Assigning a value to the variable 'jsonvalue'
                # which then will be used to decide what content type should be sent in the headers
                jsonvalue = 0

                # Creating a html text with 'Invalid name' to indicate that the name chosen it's not in available
                # and assigning it to the variable 'contents'
                contents = """
                            <html>
                  <body style="background-color: lightblue;">
                    <h1>Invalid Name</h1>
                            </body>
                            </html>
                            """
        # Whenever the resource '/chromosomeLength' is selected, this part of the program is executed
        elif '/chromosomeLength' in self.path:

            # Create a variable of class Dict which contains the parameters needed to find
            # a proper response to the client
            keyandvalue = self.convert_dict(self.path)

            # Creating a dictionary which contains the name of the species and the name of the chromosome
            Dict = {}
            Dict['name_specie'] = keyandvalue['specie']
            Dict['name_chromo'] = keyandvalue['chromo']

            # Using the key 'specie' in the Dictionary 'keyandvalue' to assign that value to the variable 'name_specie'
            name_specie = keyandvalue['specie']
            # Using the key 'chromo' in the Dictionary 'keyandvalue' to assign that value to the variable 'name_chromo'
            name_chromo = keyandvalue['chromo']

            # Define the endpoint and the headers
            ENDPOINT = "/info/assembly/" + name_specie + "?"
            headers = {'Content-Type': 'application/json'}

            # Establishing connection to the Server
            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT, None, headers)

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

            # Loop to decide whether to send a json or a html file depending if the parameter json=1 was selected or not
            if 'json=1' in self.path:

                # Assigning a value to the variable 'jsonvalue'
                # which then will be used to decide what content type should be sent in the headers
                jsonvalue = 1

                # Converting in text json the dictionary 'Dict' and assigning it to the variable 'contents'
                contents = json.dumps(Dict)

            else:
                # Assigning a value to the variable 'jsonvalue'
                # which then will be used to decide what content type should be sent in the headers
                jsonvalue = 0

                # Creating a try-catch to deal with Key errors
                try:

                    # Using the key 'top_level_region' in the Dictionary 'parameters'
                    # to assign that value to the variable 'response'
                    response = response['top_level_region']

                    # Creating a html text with the length of the chromosome and assigning it to the variable 'contents'
                    contents = """
                                <html>
                      <body style="background-color: pink;">
                        <h1>Length of the Chromosome</h1>
                                """
                    for number in response:
                        if number['name'] == name_chromo:
                            contents = contents + str(number['length'])

                    contents = contents + """
                                </body>
                                </html>
                                """
                except KeyError:

                    # Creating a html text with 'Invalid name' to indicate that the name chosen it's not in available
                    # and assigning it to the variable 'contents'
                    contents = """
                                <html>
                      <body style="background-color: lightblue;">
                        <h1>Invalid Name</h1>
                                </body>
                                </html>
                                """

        # Whenever the resource '/geneSeq' is selected, this part of the program is executed
        elif "/geneSeq" in self.path:

            # Create a variable of class Dict which contains the parameters needed to find
            # a proper response to the client
            keyandvalue = self.convert_dict(self.path)

            # Using the key 'gene' in the Dictionary 'keyandvalue' to assign that value to the variable 'gene_name'
            gene_name = keyandvalue['gene']

            # Define the endpoint and the headers
            ENDPOINT = "/homology/symbol/human/" + gene_name + "?content-type=application/json"
            headers = {'User-Agent': 'http-client'}

            # Establishing connection to the Server
            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT, None, headers)

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

            # Using the key 'data', indexing in the first position, and using the key 'id'
            # to assign that value to the variable 'id'
            id = response['data'][0]['id']

            # Establishing connection to the Server
            conn.request('GET', '/sequence/id/' + id + '?content-type=application/json')

            # Get the response
            r1 = conn.getresponse()

            # Decoding the response
            data1 = r1.read().decode('utf-8')

            # Closing the connection
            conn.close()

            # Creating a dictionary from the response received
            response = json.loads(data1)

            # Using the key 'seq' to assign that value to the variable 'DNAsequence'
            DNAsequence = response['seq']

            # Creating a dictionary which contains the sequence of DNA
            Dict = {}
            Dict['DNAsequence'] = response['seq']

            # Loop to decide whether to send a json or a html file depending if the parameter json=1 was selected or not
            if 'json=1' in self.path:

                # Assigning a value to the variable 'jsonvalue'
                # which then will be used to decide what content type should be sent in the headers
                jsonvalue = 1

                # Converting in text json the dictionary 'Dict' and assigning it to the variable 'contents'
                contents = json.dumps(Dict)

            else:
                # Assigning a value to the variable 'jsonvalue'
                # which then will be used to decide what content type should be sent in the headers
                jsonvalue = 0

                # Creating a html text with the sequence of DNA and assigning it to the variable 'contents'
                contents = """
                              <html>
                    <body style="background-color: lightgreen;">
                      <h1>DNA sequence</h1>
                        """ + DNAsequence + """
                              </body>
                              </html>
                              """
        # Whenever the resource '/geneInfo' is selected, this part of the program is executed
        elif "/geneInfo" in self.path:

            # Create a variable of class Dict which contains the parameters needed to find
            # a proper response to the client
            keyandvalue = self.convert_dict(self.path)

            # Using the key 'gene' in the Dictionary 'keyandvalue' to assign that value to the variable 'gene_name'
            gene_name = keyandvalue['gene']

            # Define the endpoint and the headers
            ENDPOINT = "/homology/symbol/human/" + gene_name + "?content-type=application/json"
            headers = {'User-Agent': 'http-client'}

            # Establishing connection to the Server
            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT, None, headers)

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

            # Using the key 'data', indexing in the first position, and using the key 'id'
            # to assign that value to the variable 'id'
            idd = response['data'][0]['id']

            # Define the endpoint and the headers
            ENDPOINT = "/overlap/id/" + idd + "?feature=gene;content-type=application/json"
            headers = {'User-Agent': 'http-client'}

            # Establishing connection to the Server
            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT, None, headers)

            # Get the response
            r1 = conn.getresponse()

            # Check The status of the response
            print('Response received: {}\n'.format(r1.status, r1.reason))

            # Decoding the response
            data1 = r1.read().decode('utf-8')

            # Closing the connection
            conn.close()

            # Creating a dictionary from the response received
            response1 = json.loads(data1)

            # Indexing in the first position and using the key 'start' to assign that value to the variable 'start'
            start = response1[0]['start']
            # Indexing in the first position and using the key 'end' to assign that value to the variable 'end'
            end = response1[0]['end']
            # Subtracting the end-start to know the length and assigning that value to the variable 'length'
            length = end - start
            # Using the key 'assembly_name' in the Dictionary 'parameters' to assign that value to the variable 'chromo'
            chromo = response1[0]['assembly_name']

            # Creating a dictionary which contains the name, start, end, and length of the chromosome
            Features = {}
            Features['start'] = response1[0]['start']
            Features['end'] = response1[0]['end']
            Features['length'] = length
            Features['chromo'] = response1[0]['assembly_name']
            Features['id'] = idd

            # Loop to decide whether to send a json or a html file depending if the parameter json=1 was selected or not
            if 'json=1' in self.path:

                # Assigning a value to the variable 'jsonvalue'
                # which then will be used to decide what content type should be sent in the headers
                jsonvalue = 1

                # Converting in text json the dictionary 'Dict' and assigning it to the variable 'contents'
                contents = json.dumps(Features)

            else:
                # Assigning a value to the variable 'jsonvalue'
                # which then will be used to decide what content type should be sent in the headers
                jsonvalue = 0

                # Creating a html text with the starting, ending, length, name of the chromosome and id of a gene
                # and assigning it to the variable 'contents'
                contents = """
                                  <html>
                        <body style="background-color: lightgreen;">
                          <h1>Information about the Gene</h1>
                            """ + 'Start:' + str(start) + '\nEnd:' + str(end) + '\nLength:' + str(
                    length) + '\nChromosome:' + chromo + '\nId:' + idd + """
                                  </body>
                                  </html>
                                  """
        # Whenever the resource '/geneCal' is selected, this part of the program is executed
        elif '/geneCal' in self.path:

            # Create a variable of class Dict which contains the parameters needed to find
            # a proper response to the client
            keyandvalue = self.convert_dict(self.path)

            # Using the key 'gene' in the Dictionary 'keyandvalue' to assign that value to the variable 'gene_name'
            gene_name = keyandvalue['gene']

            # Define the endpoint and the headers
            ENDPOINT = "/homology/symbol/human/" + gene_name + "?content-type=application/json"
            headers = {'User-Agent': 'http-client'}

            # Establishing connection to the Server
            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT, None, headers)

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

            # Using the key 'data', indexing in the first position, and using the key 'id'
            # to assign that value to the variable 'id'
            idd = response['data'][0]['id']

            # Define the endpoint and the headers
            ENDPOINT = "/sequence/id/" + idd + "?content-type=application/json"
            headers = {'User-Agent': 'http-client'}

            # Establishing connection to the Server
            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT, None, headers)

            # Get the response
            r1 = conn.getresponse()

            # Check The status of the response
            print('Response received: {}\n'.format(r1.status, r1.reason))

            # Decoding the response
            data1 = r1.read().decode('utf-8')

            # Creating a dictionary from the response received
            response = json.loads(data1)

            # Using the key 'seq' to assign that value to the variable 'DNAsequence'
            DNAsequence = response['seq']

            # Creating an object of class Seq
            seq = Seq(DNAsequence)

            # Measuring the len of the sequence and assigning that value to the variable 'length'
            length = len(DNAsequence)

            # Calculating the percentage od each base using the class Seq
            perc_A = seq.perc('A')
            perc_C = seq.perc('C')
            perc_T = seq.perc('T')
            perc_G = seq.perc('G')

            # Creating a dictionary which contains the length of the sequence and the percentage of each base
            Calculations = {}
            Calculations['length'] = length
            Calculations['Perc_A'] = perc_A
            Calculations['Perc_c'] = perc_C
            Calculations['Perc_T'] = perc_T
            Calculations['Perc_G'] = perc_G

            # Loop to decide whether to send a json or a html file depending if the parameter json=1 was selected or not
            if 'json=1' in self.path:

                # Assigning a value to the variable 'jsonvalue'
                # which then will be used to decide what content type should be sent in the headers
                jsonvalue = 1

                # Converting in text json the dictionary 'Dict' and assigning it to the variable 'contents'
                contents = json.dumps(Calculations)

            else:
                # Assigning a value to the variable 'jsonvalue'
                # which then will be used to decide what content type should be sent in the headers
                jsonvalue = 0

                # Creating a html text with the length, and percentage of each base of a gene
                # and assigning it to the variable 'contents'
                contents = """
                                  <html>
                        <body style="background-color: lightgreen;">
                          <h1>Total Lenght and Percentage of each Base</h1>
                            """ + 'Lenght' + str(length) + '<br>' + "Percentage of A's" + \
                           str(perc_A) + '<br>' + "Percentage of C's" + str(perc_C) + '<br>' + "Percentage of T's" + str(
                    perc_T) + '<br>' + "Percentage of G's: " + str(perc_G) +\
                                    """
                                  </body>
                                  </html>
                                  """
        # Whenever the resource '/geneList' is selected, this part of the program is executed
        elif '/geneList' in self.path:

            # Create a variable of class Dict which contains the parameters needed to find
            # a proper response to the client
            keyandvalue = self.convert_dict(self.path)

            # Using the key 'chromo' in the Dictionary 'keyandvalue' to assign that value to the variable 'chromo'
            chromo = keyandvalue['chromo']

            # Using the key 'start' in the Dictionary 'keyandvalue' to assign that value to the variable 'start'
            start = keyandvalue['start']

            # Using the key 'end' in the Dictionary 'keyandvalue' to assign that value to the variable 'end'
            end = keyandvalue['end']

            # Define the endpoint and the headers
            ENDPOINT = "/overlap/region/human/" + str(chromo) + ":" + str(start) + "-" + str(end) + "?content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon"
            headers = {'User-Agent': 'http-client'}

            # Establishing connection to the Server
            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT, None, headers)

            # Get the response
            response = conn.getresponse()

            # Check The status of the response
            print('Response received: {}\n'.format(response.status, response.reason))

            # Decoding the response
            data = response.read().decode("utf-8")

            # Closing the connection
            conn.close()

            # Creating a dictionary from the response received
            response2 = json.loads(data)

            # Creating a variable which determine when the loop should break
            stop = int(end) - int(start)

            # Define a counter and an list which after going over the loop will contain the names of the genes
            count = 0
            List = []

            # Loop for going over the list of possible genes and taking their names until the limit has been reached
            for possiblegene in response2:

                if possiblegene['feature_type'] == 'gene':

                    List.append(possiblegene['external_name'])

                    count = count + 1
                    if count == stop:
                        break

            # Creating a dictionary which contains the names of the genes in a precise segment of a chromosome
            Dict = {}
            Dict['Gene'] = List

            # Loop to decide whether to send a json or a html file depending if the parameter json=1 was selected or not
            if 'json=1' in self.path:

                # Assigning a value to the variable 'jsonvalue'
                # which then will be used to decide what content type should be sent in the headers
                jsonvalue = 1

                # Converting in text json the dictionary 'Dict' and assigning it to the variable 'contents'
                contents = json.dumps(Dict)

            else:
                # Assigning a value to the variable 'jsonvalue'
                # which then will be used to decide what content type should be sent in the headers
                jsonvalue = 0

                # Creating a html text with the names of the genes located in a specific region in a chromosome
                # and assigning it to the variable 'contents'
                contents = """
                                                <html>
                                      <body style="background-color: green;">
                                        <h1>Name of Each Gene</h1>
                                                <ul>"""
                count = 0
                for possiblegene in response2:
                    if possiblegene['feature_type'] == 'gene':
                        contents = contents + '<li>' + possiblegene['external_name'] + '</li>'
                        count = count + 1

                        if count == stop:
                            break
                contents = contents + """
                                                </ul>
                                                </body>
                                                </html>
                                                """

        # Whenever the resource none of the above resources is selected, this part of the program is executed
        else:
            # Assigning a value to the variable 'jsonvalue'
            # which then will be used to decide what content type should be sent in the headers
            jsonvalue = 0

            # Assigning to the variable contents the name of the 'error.html' file
            contents = 'error.html'

            # Open the file and read its content
            with open(contents, 'r') as a:
                contents = a.read()
                a.close()

        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        # Creating a loop to choose what 'content type' in headers should be added
        if jsonvalue == 1:
            # Define the content-type header:
            self.send_header('Content-Type', 'application/json')

        else:
            # Define the content-type header:
            self.send_header('Content-Type', 'text/html')

        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# Main Program

# -- Set the new handler
Handler = TestHandler
socketserver.TCPServer.allow_reuse_address = True

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- client, the handler is called

    # Try-catch to deal with KeyboardInterrupt errors
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()
