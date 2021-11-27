import requests
import json

class Api:
    def __init__(self):
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        self.s  = requests.Session()
        self.s.headers.update(headers)

    def get(self, url, data=''):
        response = self.s.get(url=url, data=data)
        self.__checkStatus(response)
        return response  

    def post(self, url, data=''):
        response = self.s.post(url=url, data=data)
        self.__checkStatus(response)
        return response

    def put(self, url, data):
        response = self.s.put(url=url, data=data)
        self.__checkStatus(response)

    def delete(self, url):
        response = self.s.delete(url=url)
        self.__checkStatus(response)

    # Checks the status code from the html request and exits
    #   the program if the operation was not successful
    def __checkStatus(self, response):
        if response.status_code >= 200 and response.status_code <= 206:
            return
        elif response.status_code == 404:
            print("Response 404, URI not found")
        elif response.status_code == 400:
            print("Response 400, Bad request")
        else:
            print("Operation returned non success status: " + str(response.status_code))
            print("Error contents, if they exist: " + str(response.text))
            pprint.pprint(vars(response))
        sys.exit(1)

    # Most items are given a name when created, but
    #  need to specified by ID when used to create other items
    #  This function looks up an item by its name and returns
    #  the ID
    def getIDFromName(self, url, key, name):
        response = self.s.get(url=url)
        # This is great if you need to view every piece of the response
        #   when debugging
        # print()
        # pprint.pprint(vars(response))
        # print()

        reply = json.loads(response.text)

        # pprint.pprint(reply)

        if isinstance(reply, list):
            for item in reply:
                if item[key] == name:
                    # print("Found ID: " + str(item["id"]))
                    return item["id"]
        elif isinstance(reply, dict):
            if reply.get(key) == name:
                #print("Found ID: " + str(reply["id"]))
                return reply["id"]

        #print("ID not found")
        return None


