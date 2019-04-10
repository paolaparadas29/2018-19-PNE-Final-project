import socketserver
import termcolor
import http.server
import http.client
import json
from Seq import Seq

# Define the server's port and hostname

HOSTNAME = "rest.ensembl.org"
METHOD = "GET"
PORT = 8000
SERVER = "rest.ensembl.org"


class TestHandler(http.server.BaseHTTPRequestHandler):

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

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line

        termcolor.cprint(self.requestline, 'green')

        # Selecting type

        if self.path == '/':
            json = 0
            contents = 'index.html'
            with open(contents, 'r') as a:
                contents = a.read()
                a.close()

        elif '/listSpecies?limit' in self.path:
            parameters = self.convert_dict(self.path)
            print(parameters)

            try:
                limit = parameters['limit']

                ENDPOINT = "/info/species?content-type=application/json"
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPConnection(HOSTNAME)
                conn.request(METHOD, ENDPOINT, None, headers)
                r1 = conn.getresponse()
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                text_json = r1.read().decode("utf-8")
                conn.close()

                list1 = json.loads(text_json)
                list_of_species = list1['species']

            except ValueError:

                ENDPOINT = "/info/species?content-type=application/json"
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPConnection(HOSTNAME)
                conn.request(METHOD, ENDPOINT, None, headers)
                r1 = conn.getresponse()
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                text_json = r1.read().decode("utf-8")
                conn.close()

                list1 = json.loads(text_json)
                list_of_species = list1['species']
                limit = len(list_of_species)


            except TypeError:

                ENDPOINT = "/info/species?content-type=application/json"
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPConnection(HOSTNAME)
                conn.request(METHOD, ENDPOINT, None, headers)
                r1 = conn.getresponse()
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                text_json = r1.read().decode("utf-8")
                conn.close()

                list1 = json.loads(text_json)
                list_of_species = list1['species']
                limit = len(list_of_species)

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

            if 'json=1' in parameters:
                json = 1
                contents = json.dumps(Dict)
            else:
                json=0

                if int(limit) <= len(list_of_species):

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

                else:
                    limit = len(list_of_species)

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

        elif '/karyotype' in self.path:
            parameters = self.convert_dict(self.path)

            try:
                a = parameters['specie']

                ENDPOINT = "/info/assembly/" + a + "?"

                headers = {'Content-Type': 'application/json'}
                conn = http.client.HTTPConnection(HOSTNAME)
                conn.request(METHOD, ENDPOINT, None, headers)
                r1 = conn.getresponse()

                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                text_json = r1.read().decode("utf-8")
                conn.close()

                response = json.loads(text_json)
                karyotype = response['karyotype']
                karyotype_specie = {}
                karyotype_specie['karyotype'] = response['karyotype']

                if 'json=1' in parameters:
                    json=1
                    contents = json.dumps(karyotype_specie)
                else:
                    json=0

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

        elif '/chromosomeLenght' in self.path:

            parameters = self.convert_dict(self.path)

            parameter={}
            parameter['name_specie']= parameters['specie']
            parameter['name_chromo']= parameters['chromo']

            name_specie = parameters['specie']
            name_chromo = parameters['chromo']

            # if 'specie' in parameters and 'chromo' in parameters:

            ENDPOINT = "/info/assembly/" + name_specie + "?"
            headers = {'Content-Type': 'application/json'}
            conn = http.client.HTTPConnection(HOSTNAME)
            conn.request(METHOD, ENDPOINT, None, headers)
            r1 = conn.getresponse()

            print('Response received: {}\n'.format(r1.status, r1.reason))
            data1 = r1.read().decode('utf-8')
            response = json.loads(data1)

            if 'json=1' in parameters:
                json=1
                contents = json.dumps(parameter)
            else:
                json=0

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

        elif "/geneSeq" in self.path:
            parameters = self.convert_dict(self.path)

            gene_name = parameters['gene']

            conn = http.client.HTTPConnection(HOSTNAME, PORT)
            conn.request("GET", "/homology/symbol/human/" + gene_name + "?content-type=application/json")

            r1 = conn.getresponse()
            print('Response received: {}\n'.format(r1.status, r1.reason))
            data1 = r1.read().decode('utf-8')
            response = json.loads(data1)
            id = response['data'][0]['id']

            conn.request('GET', '/sequence/id/' + id + '?content-type=application/json')
            r1 = conn.getresponse()
            data1 = r1.read().decode('utf-8')
            response = json.loads(data1)

            DNAsequence = response['seq']

            DNAsequence_json = {}
            DNAsequence_json['DNAsequence'] = response['seq']

            if 'json=1' in parameters:
                json=1
                contents = json.dumps(DNAsequence_json)
            else:
                json=0

                contents = """
                              <html>
                    <body style="background-color: lightgreen;">
                      <h1>DNA sequence</h1>
                        """ + DNAsequence + """
                              </body>
                              </html>
                              """

        elif "/geneInfo" in self.path:
            parameters = self.convert_dict(self.path)

            gene_name = parameters['gene']

            conn = http.client.HTTPConnection(SERVER, PORT)
            conn.request("GET", "/homology/symbol/human/" + gene_name + "?content-type=application/json")
            r1 = conn.getresponse()
            print('Response received: {}\n'.format(r1.status, r1.reason))
            data1 = r1.read().decode('utf-8')
            response = json.loads(data1)
            id = response['data'][0]['id']

            conn = http.client.HTTPConnection(HOSTNAME, PORT)
            conn.request("GET", "/overlap/id/" + id + "?feature=gene;content-type=application/json")
            r1 = conn.getresponse()
            print('Response received: {}\n'.format(r1.status, r1.reason))
            data1 = r1.read().decode('utf-8')
            response1 = json.loads(data1)
            start = response1[0]['start']
            end = response1[0]['end']
            length = end - start
            chromo = response1[0]['assembly_name']

            Features = {}
            Features['start']= response1[0]['start']
            Features['end'] = response1[0]['end']
            Features['length'] = length
            Features['chromo']= response1[0]['assembly_name']

            if 'json=1' in parameters:
                json = 1
                contents = json.dumps(Features)
            else:
                json = 0

                contents = """
                                  <html>
                        <body style="background-color: lightgreen;">
                          <h1>Information about the Gene</h1>
                            """ + 'Start:' + str(start) + 'End:' + str(end) + 'Length:' + str(
                    length) + 'Chromosome:' + chromo + """
                                  </body>
                                  </html>
                                  """
        elif '/geneCal' in self.path:
            parameters = self.convert_dict(self.path)

            gene_name = parameters['gene']

            conn = http.client.HTTPConnection(HOSTNAME, PORT)
            conn.request("GET", "/homology/symbol/human/" + gene_name + "?content-type=application/json")

            r1 = conn.getresponse()
            print('Response received: {}\n'.format(r1.status, r1.reason))
            data1 = r1.read().decode('utf-8')
            response = json.loads(data1)
            id = response['data'][0]['id']

            conn.request('GET', '/sequence/id/' + id + '?content-type=application/json')
            r1 = conn.getresponse()
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
            Calculations['length']= length
            Calculations['Perc_A']= perc_A
            Calculations['Perc_c']= perc_C
            Calculations['Perc_T']= perc_T
            Calculations['Perc_G']= perc_G

            if 'json=1' in parameters:
                json = 1
                contents = json.dumps(Calculations)
            else:
                json = 0

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

        elif '/geneList' in self.path:
            parameters = self.convert_dict(self.path)

            chromo = parameters['chromo']
            start = parameters['start']
            end = parameters['end']

            conn = http.client.HTTPConnection(HOSTNAME, PORT)
            conn.request(METHOD, "/overlap/region/human/" + str(chromo) + ":" + str(start) + "-" + str(
                end) + "?content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon")
            response = conn.getresponse()
            data = response.read().decode("utf-8")
            response2 = json.loads(data)

            count = 0
            List = []
            for possiblegene in response2:
                if possiblegene['feature_type'] == 'gene':
                    name = possiblegene['external_name']
                    start = possiblegene['start']
                    end = possiblegene['end']
                    List.extend('Name:', name , 'Start:', start, 'End:', end)

                    count = count + 1
                    if int(count) == int(end - start):
                        break

            Dict = {}
            Dict['Gene'] = List

            if 'json=1' in parameters:
                json=1
                contents = json.dumps(Dict)
            else:
                json=0
                contents = """
                                                <html>
                                      <body style="background-color: green;">
                                        <h1>Information of Each Gene</h1>
                                                <ul>"""
                count = 0
                for possiblegene in response2:
                    if possiblegene['feature_type'] == 'gene':
                        contents = contents + '<li>' + possiblegene['external_name'] + " " + str(
                            possiblegene['start']) + " " + str(possiblegene['end']) + '</li>'
                        count = count + 1

                        if int(count) == int(end - start):
                            break
                contents = contents + """
                                                </ul>
                                                </body>
                                                </html>
                                                """
        else:
            contents = 'error.html'
            with open(contents, 'r') as a:
                contents = a.read()
                a.close()

        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        if json == 1:
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
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stopped by the user")
        httpd.server_close()
