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
        dictionary = dict()
        keyvalue = path.split('?')[1]
        keyvalue = keyvalue.split(' ')[0]
        listt = keyvalue.split('&')

        # Loop for iterating over the different values in the list 'listt' to fill the dictionary
        for keyandvalue in listt:
            key = keyandvalue.split('=')[0]
            value = keyandvalue.split('=')[1]
            dictionary[key] = value

        return dictionary

    # A method is called whenever the client invokes the GET method in the HTTP protocol request
    def do_GET(self):

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # Selecting type of resource that must be used to create the response to the client

        # Whenever the resource '/' is selected, this part of the program is executed
        if self.path == '/':

            jsonvalue = 0
            contents = 'index.html'
            # Open the file and read the content in the index
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
                    parameters = self.convert_dict(self.path)

                    # Using the key 'limit' in the Dictionary 'parameters' to assign that value to the variable 'limit'
                    limit = parameters['limit']

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
                    list1 = json.loads(text_json)

                    # Creating a list with the species
                    list_of_species = list1['species']

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
                    list1 = json.loads(text_json)

                    # Creating a list with the species
                    list_of_species = list1['species']

                    # Assigning the value of the number of all the species to the variable limit to deal with this error
                    limit = len(list_of_species)

                # This try-catch deals with value errors
                try:
                    int(limit)
                except ValueError:
                    limit = len(list_of_species)

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
                list1 = json.loads(text_json)

                # Creating a list with the species
                list_of_species = list1['species']

                # Assigning the value of the number of all the species to the variable limit to deal with this error
                limit = len(list_of_species)


            # Define a counter and an list which after the loop will contain the names of the species
            count = 0
            List = []

            # Loop for going over the list of species and taking their names until the limit has been reached
            for one in list_of_species:
                specie = one['name']
                List.append(specie)
                count = count + 1

                if int(count) == int(limit):
                    break

            #Creating a dictionary which contains the name of the species
            Dict = {}
            Dict['List_of_species'] = List

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
                for one in list_of_species:
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
            parameters = self.convert_dict(self.path)

            # This try-catch deals with key errors
            try:
                # Using the key 'specie' in the Dictionary -parameters- to assign that value to the variable 'name'
                name = parameters['specie']

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


                karyotype = response['karyotype']
                karyotype_specie = {}
                karyotype_specie['karyotype'] = response['karyotype']

                if 'json=1' in self.path:
                    jsonvalue = 1
                    contents = json.dumps(karyotype_specie)
                else:
                    jsonvalue = 0

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
            parameters = self.convert_dict(self.path)

            parameter = {}
            parameter['name_specie'] = parameters['specie']
            parameter['name_chromo'] = parameters['chromo']

            # Using the key 'specie' in the Dictionary -parameters- to assign that value to the variable 'name_specie'
            name_specie = parameters['specie']
            # Using the key 'chromo' in the Dictionary -parameters- to assign that value to the variable 'name_chromo'
            name_chromo = parameters['chromo']

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


            response = json.loads(data1)

            if 'json=1' in self.path:
                jsonvalue = 1
                contents = json.dumps(parameter)
            else:
                jsonvalue = 0

                try:

                    response = response['top_level_region']

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
            parameters = self.convert_dict(self.path)

            # Using the key 'gene' in the Dictionary -parameters- to assign that value to the variable 'gene_name'
            gene_name = parameters['gene']

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
            data1 = r1.read().decode('utf-8')
            response = json.loads(data1)
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

            DNAsequence = response['seq']

            DNAsequence_json = {}
            DNAsequence_json['DNAsequence'] = response['seq']

            if 'json=1' in self.path:
                jsonvalue = 1
                contents = json.dumps(DNAsequence_json)
            else:
                jsonvalue = 0

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
            parameters = self.convert_dict(self.path)

            # Using the key 'gene' in the Dictionary -parameters- to assign that value to the variable 'gene_name'
            gene_name = parameters['gene']

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
            response = json.loads(data1)
            id = response['data'][0]['id']

            # Define the endpoint and the headers
            ENDPOINT = "/overlap/id/" + id + "?feature=gene;content-type=application/json"
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


            start = response1[0]['start']
            end = response1[0]['end']
            length = end - start
            chromo = response1[0]['assembly_name']

            Features = {}
            Features['start'] = response1[0]['start']
            Features['end'] = response1[0]['end']
            Features['length'] = length
            Features['chromo'] = response1[0]['assembly_name']
            Features['id'] = id

            if 'json=1' in self.path:
                jsonvalue = 1
                contents = json.dumps(Features)
            else:
                jsonvalue = 0

                contents = """
                                  <html>
                        <body style="background-color: lightgreen;">
                          <h1>Information about the Gene</h1>
                            """ + 'Start:' + str(start) + '\nEnd:' + str(end) + '\nLength:' + str(
                    length) + '\nChromosome:' + chromo + '\nId:' + id + """
                                  </body>
                                  </html>
                                  """
        # Whenever the resource '/geneCal' is selected, this part of the program is executed
        elif '/geneCal' in self.path:

            # Create a variable of class Dict which contains the parameters needed to find
            # a proper response to the client
            parameters = self.convert_dict(self.path)

            # Using the key 'gene' in the Dictionary -parameters- to assign that value to the variable 'gene_name'
            gene_name = parameters['gene']

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
            id = response['data'][0]['id']

            # Define the endpoint and the headers
            ENDPOINT = "/sequence/id/" + id + "?content-type=application/json"
            headers = {'User-Agent': 'http-client'}

            # Establishing connection to the Server
            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT, None, headers)

            # Get the response
            r1 = conn.getresponse()

            # Check The status of the response
            print('Response received: {}\n'.format(r1.status, r1.reason))

            data1 = r1.read().decode('utf-8')

            response = json.loads(data1)

            DNAsequence = response['seq']

            seq = Seq(DNAsequence)
            length = len(DNAsequence)
            perc_A = seq.perc('A')
            perc_C = seq.perc('C')
            perc_T = seq.perc('T')
            perc_G = seq.perc('G')

            Calculations = {}
            Calculations['length'] = length
            Calculations['Perc_A'] = perc_A
            Calculations['Perc_c'] = perc_C
            Calculations['Perc_T'] = perc_T
            Calculations['Perc_G'] = perc_G

            if 'json=1' in self.path:
                jsonvalue = 1
                contents = json.dumps(Calculations)
            else:
                jsonvalue = 0

                contents = """
                                  <html>
                        <body style="background-color: lightgreen;">
                          <h1>Total Lenght and Percentage of each Base</h1>
                            """ + 'Lenght' + str(length) + '<br>' + "Percentage of A's" + \
                           str(perc_A) + '<br>' + "Percentage of C's" + str(
                    perc_C) + '<br>' + "Percentage of T's" + str(
                    perc_T) \
                           + '<br>' + "Percentage of G's: " + str(perc_G) + """
                                  </body>
                                  </html>
                                  """
        # Whenever the resource '/geneList' is selected, this part of the program is executed
        elif '/geneList' in self.path:

            # Create a variable of class Dict which contains the parameters needed to find
            # a proper response to the client
            parameters = self.convert_dict(self.path)

            # Using the key 'chromo' in the Dictionary -parameters- to assign that value to the variable 'chromo'
            chromo = parameters['chromo']

            # Using the key 'start' in the Dictionary -parameters- to assign that value to the variable 'start'
            start = parameters['start']

            # Using the key 'end' in the Dictionary -parameters- to assign that value to the variable 'end'
            end = parameters['end']

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


            response2 = json.loads(data)

            stop = int(end) - int(start)

            count = 0
            List = []
            for possiblegene in response2:
                print(possiblegene)
                if possiblegene['feature_type'] == 'gene':

                    List.append(possiblegene['external_name'])

                    count = count + 1
                    if count == stop:
                        break

            Dict = {}
            Dict['Gene'] = List

            if 'json=1' in self.path:
                jsonvalue = 1
                contents = json.dumps(Dict)
            else:
                jsonvalue = 0
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
            contents = 'error.html'
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
