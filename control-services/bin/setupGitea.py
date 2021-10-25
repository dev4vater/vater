#!/usr/bin/env python3
import requests
import json
import time
import getpass
import os

# Checks the status code from the html request and exits
#   the program if the operation was not successful
def checkStatus(response):
    # Debugging tool
    print()
    print(vars(response))
    print()
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
    # print()
    print(vars(response))
    # print()
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

    # The local filepath for ROUS in the Gitea container
    configurationRepositoryPath = "/data/git/rous"

    # User for configurations and administration
    configurationUser = "config"

    ### TOP LEVEL VARIABLES ###
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    s = requests.Session()
    sessionToken = ""
    cleanSessionToken = False

    print("-----GITEA CONFIGURATION")

    tokenID = getIDFromName(s, url, headers, "configurationToken")

    exit()

    stream = os.popen("sudo docker exec -it gitea su git bash -c"       + \
                      "\"gitea admin user list "                        + \
                      "| grep " + configurationUser                     + \
                      "| tr -s ' ' "                                    + \
                      "| cut -d ' ' -f 2\"")

    user = stream.read()

    print("---LOGGING IN")

    if user != configurationUser:
        print("---CREATING " + configurationUser + " USER")
        passwd = getpass.getpass(prompt="Password: ")
        os.system("sudo docker exec -it gitea su git bash -c"               + \
                  "\"gitea admin user create --admin"                       + \
                  "--username " + user                                      + \
                  "--email + fake@a.a "                                     + \
                  "--password" + passwd                                     + \
                  "--must-change-password=false\"")
    else:
        print("---FOUND " + configurationUser + " USER")
        splitHost = host.split("//")
        api = "/users/" + configurationUser + "/tokens"

        while True:
            passwd = getpass.getpass(prompt="Password: ")

            url = splitHost[0] + user + ":" + passwd + "@" + splitHost[1] + api

            response = s.post(url=host+api, headers=headers, data=data, verify=False)

                if response.status_code != 401:
                    break

    exit()

    print("---CHECKING FOR TOKEN")

    tokenID = getIDFromName(s, url, headers, "configurationToken")

    if tokenID == None:

        print("---CREATING TOKEN")

        api = "/users/" + configurationUser + "/tokens"

        data = '{"name": "configurationToken"}'
#        response = s.post(url=host+api, headers=headers, data=data, verify=False)
        response = s.post(url=host+api, headers=headers, data=data, verify=False, auth=('config', 'config'))
        checkStatus(response)

        sessionToken = json.loads(response.text)["sha1"]
        print(sessionToken)

        tokenID = getIDFromName(s, url, headers, "configurationToken")

    # New headers with the token
    authHeaders = {
        "Accept": "application/json",
        "Authorization": "token " + sessionToken,
        "Content-Type": "application/json"
    }

    print("---CREATING 333TRS ORGANIZATION")

    api = "/orgs"
    data =  '{'                              +\
            '"username": "333TRS"'           +\
            '}'
    print(data)

    response = s.post(url=host+api, headers=authHeaders, verify=False, data=data)
    checkStatus(response)

    print("---CREATING ROUS REPOSITORY ")

    api = "/repos/migrate"
#    data = '{ "auth_token": "token ' + sessionToken + '", ' + \
    data = '{ "clone_addr": "' + configurationRepositoryPath + '", ' + \
           '"repo_name": "rous", ' + \
           '"repo_owner": "333TRS" }'
    print(data)

    response = s.post(url=host+api, headers=authHeaders, verify=False, data=data)
    checkStatus(response)

    print("---REVOKING TOKEN")

    api = "/users/" + configurationUser + "/tokens/" + str(tokenID)

    response = s.delete(url=host+api, headers=headers, verify=False, auth=('config', 'config'))
    checkStatus(response)

if __name__ == "__main__":
    main()
