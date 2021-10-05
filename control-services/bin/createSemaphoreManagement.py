#!/usr/bin/env python3
import requests
import json

# Checks the status code from the html request and exits
#   the program if the operation was not successful
def checkStatus(response):
    if response.status_code == 204 or response.status_code == 200:
        print("Success")
        return
    elif response.status_code == 404:
        print("Response 404, URI not found")
    elif response.status_code == 400:
        print("Response 400, Bad request")
    else:
        print("Operation returned non success status: " + str(response.status_code))
        print("Error contents, if they exist: " + str(response.text))
    exit()

def main():
    # Configuration items
    host = "http://localhost:4000/api"
    playbookRepositoryUrl = "http://192.168.100.1:3000/uwardlaw/playbook-repo.git"

    # Top level variables
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    s = requests.Session()
    sessionToken = ""
    cleanSessionToken = False
    createManagementProject = True
    managementProjectID = -1
    repositoryKeyID = -1

    print("---LOGINING IN")
    api = "/auth/login"
    data = '{"auth":"admin", "password":"cangetin"}'
    response = s.post(url=host+api, headers=headers, data=data)

#    t = "1lh0lppoehqdw0msbkp79xg3nqlqcaeittjlus1-8zw="
#    response = s.delete(url="http://localhost:4000/api/user/tokens/"+t, headers=headers)
#    print("Adhoc delete, response: ")
#    print(response)
#    exit()

    print("---CHECKING FOR ACTIVE TOKENS")
    api = "/user/tokens"
    response = s.get(url=host+api, headers=headers)
    checkStatus(response)

    tokens = json.loads(response.text)
    for token in tokens:
        if token["expired"] == False:
            print(token)
            id = token["id"]
            print("Found active token: " + id)
            sessionToken = id
    if sessionToken == "":
        print("No active tokens found")

    print("---GENERATING TOKEN IF NEEDED")
    api = "/user/tokens"

    if sessionToken == "":
        response = s.post(url=host+api, headers=headers)
        generatedToken = json.loads(response.text)["id"]
        print("Generated: " + generatedToken)
        sessionToken = generatedToken
        cleanSessionToken = True

    # Check to see if there is a project called Management
    #   and if there is, exit the program
    print("---CHECKING FOR MANAGEMENT PROJECT")
    api = "/projects"
    response = s.get(url=host+api, headers=headers)
    checkStatus(response)

    projects = json.loads(response.text)
    for project in projects:
        if project["name"] == "Management":
            print("Found Management Project")
            createManagementProject = False
            #exit()

    # Create a project if one did not exist
    if createManagementProject == True:
        print("---CREATING MANAGEMENT PROJECT")
        api = "/projects"
        data = '{"name":"Management", "alert":false}'
        response = s.post(url=host+api, headers=headers, data=data)
        checkStatus(response)

    # Get the ID for the project just created
    print("---GET MANAGEMENT PROJECT ID")
    response = s.get(url=host+api, headers=headers)
    checkStatus(response)
    projects = json.loads(response.text)
    for project in projects:
        if project["name"] == "Management":
            managementProjectID = project["id"]

    # Add none key type
    print("---ADD KEY OF TYPE NONE")
    api = "/project/" + str(managementProjectID) + "/keys"
    data = '{"name": "None", "type": "None", "project_id": ' + str(managementProjectID) + '}'
    response = s.post(url=host+api, headers=headers, data=data)
    checkStatus(response)

    # Get the none key type ID
    print("---GET NONE KEY ID")
    api = "/project/" + str(managementProjectID) + "/keys"
    response = s.get(url=host+api, headers=headers)
    checkStatus(response)
    keys = json.loads(response.text)
    for key in keys:
        if key["name"] == "None":
            repositoryKeyID = key["id"]
    print("repo key id: " + str(repositoryKeyID))

    # Add repo
    print("---ADD PLAYBOOK REPOSITORY")
    api = "/project/"+str(managementProjectID)+"/repositories"
    data = '{"name": "Playbook repo", "project_id": ' + str(managementProjectID) + ', "git_url": "' + str(playbookRepositoryUrl) + '", "ssh_key_id": ' + str(repositoryKeyID) + '}'
    print(data)
    response = s.post(url=host+api, headers=headers, data=data)
    checkStatus(response)

    # Add inventory
    # Add env

    print("---ATTEMPTING TO CLEAN GENERATED TOKEN")
    api = "/user/tokens"

    if cleanSessionToken == True:
        print("Trying to clean")
        response = s.delete(url=host+api+'/'+sessionToken, headers=headers)
        checkStatus(response)
        print("Deleted: " + sessionToken)
    else:
        print("No token to clean")

if __name__ == "__main__":
    main()
