#!/usr/bin/env python3
import requests
import json
import time
import getpass

# Checks the status code from the html request and exits
#   the program if the operation was not successful
def checkStatus(response):
    # Debugging tool
    # print(vars(response))
    if response.status_code >= 200 and response.status_code <= 206:
        return
    else:
        print("Operation returned non success status: " + str(response.status_code))
        print("Error message, if they exist: " + str(response.content))
    exit()

# Most items are given a name when created, but
#  need to specified by ID when used to create other items
#  This function looks up an item by its name and returns
#  the ID
def getIDFromName(s, url, headers, name):
    response = s.get(url=url, headers=headers)
    # This is great if you need to view every piece of the response
    #   when debugging
    # print(vars(response))
    dict = json.loads(response.text)
    for item in dict:
        if item["name"] == name:
            print("Found ID: " + str(item["id"]))
            return item["id"]

    print("ID not found")
    return None

def main():
    ### CONFIGURATION ITEMS ###

    # The gitea host URL
    host = "http://localhost:3000/api/v1"

    # The URL for the ROUS repo
    playbookRepositoryUrl = "http://github.com/uwardlaw/rous.git"

    ### TOP LEVEL VARIABLES ###
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    s = requests.Session()
    sessionToken = ""
    cleanSessionToken = False
    configurationUser = "config"


    print("-----GITEA CONFIGURATION")

    print("---CHECKING FOR TOKEN")

    url = "http://config:config@localhost:3000/api/v1/users/config/tokens"

    tokenID = getIDFromName(s, url, headers, "configurationToken")

    if tokenID == None:

        print("---CREATING TOKEN")

        api = "/users/" + configurationUser + "/tokens"

        data = '{"name": "configurationToken"}'
        response = s.post(url=host+api, headers=headers, data=data, verify=False, auth=('config', 'config'))

        tokenID = getIDFromName(s, url, headers, "configurationToken")

if __name__ == "__main__":
    main()
