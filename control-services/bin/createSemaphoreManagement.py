#!/usr/bin/env python3
import requests
import json
import time

# Checks the status code from the html request and exits
#   the program if the operation was not successful
def checkStatus(response):
    if response.status_code >= 200 and response.status_code <= 206:
        return
    elif response.status_code == 404:
        print("Response 404, URI not found")
    elif response.status_code == 400:
        print("Response 400, Bad request")
    else:
        print("Operation returned non success status: " + str(response.status_code))
        print("Error contents, if they exist: " + str(response.text))
    exit()

# Most items are given a name when created, but
#  need to specified by ID when used to create other items
#  This function looks up an item by its name and returns
#  the ID
def getIDFromName(s, url, headers, name):
    response = s.get(url=url, headers=headers)
    checkStatus(response)

    dict = json.loads(response.text)
    for item in dict:
        if item["name"] == name:
            print("Found ID: " + str(item["id"]))
            return item["id"]

    print("ID not found")
    return None

def createTaskTemplate(
    s, url, headers,
    templateName, playbookPath,
    projectID, repositoryID, repositoryKeyID,
    inventoryID, environmentID):

    # Check to see if the template exists
    templateID = getIDFromName(s=s, url=host+api, headers=headers, name=templateName)

    if templateID == None:
        print("---CREATING TEMPLATE: " + templateName)

        data = '{"name": "EmptyEnvironment", ' +                     \
               '"project_id": ' + str(managementProjectID) + ', ' +  \
               '"json": "{}"} '

'{"id": 0, ' +
  '"ssh_key_id": 0, ' +
  '"project_id": 0, ' +
  '"inventory_id": 0, ' +
  '"repository_id": 0, ' +
  '"environment_id": 0, ' +
  '"alias": "string", ' +
  '"playbook": "string", ' +
  '"arguments": "string", ' +
  '"override_args": true} ' +

        response = s.post(url=host+api, headers=headers, data=data)
        checkStatus(response)

        environmentID = getIDFromName(s=s, url=host+api, headers=headers, name="EmptyEnvironment")    


def main():
    ### CONFIGURATION ITEMS ###

    # The semaphore host URL
    host = "http://localhost:4000/api"

    # The URL for the git repo holding the playbooks
    playbookRepositoryUrl = "http://192.168.100.1:3000/uwardlaw/playbook-repo.git"

    # The relative path from the playbook repository to the inventory file
    #  This will usually just be the name of the inventory file if the
    #  if the inventory file sits in the root directory
    inventoryFilePath = "vm.vmware.yml"

    ### TOP LEVEL VARIABLES ###
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    s = requests.Session()
    sessionToken = ""
    cleanSessionToken = False

    managementProjectID = None
    repositoryID = None
    repositoryKeyID = None
    inventoryID = None
    environmentID = None

    print("---LOGINING IN")
    api = "/auth/login"
    data = '{"auth":"admin", "password":"cangetin"}'
    response = s.post(url=host+api, headers=headers, data=data)

     # Code to delete one off token-- useful if a token was generated
     #  but the code didn't complete during dev, so the token was left

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

    managementProjectID = getIDFromName(s=s, url=host+api, headers=headers, name="Management")
    if (managementProjectID == None):
        print("---CREATING MANAGEMENT PROJECT")

        data = '{"name":"Management", "alert":false}'
        response = s.post(url=host+api, headers=headers, data=data)
        checkStatus(response)

        managementProjectID = getIDFromName(s=s, url=host+api, headers=headers, name="Management")

    # Check to see if the key of type None exists bedore creating it
    print("---CHECKING FOR KEY ID OF TYPE NONE")
    api = "/project/" + str(managementProjectID) + "/keys"

    repositoryKeyID = getIDFromName(s=s, url=host+api, headers=headers, name="NoneKey")

    if repositoryKeyID == None:

        # Create the key
        print("---CREATING KEY OF TYPE NONE")
        data = '{"name": "NoneKey", ' +                               \
               '"type": "None", ' +                                   \
               '"project_id": ' + str(managementProjectID) + '}'
        response = s.post(url=host+api, headers=headers, data=data)
        checkStatus(response)

        # Get the created key ID
        repositoryKeyID = getIDFromName(s=s, url=host+api, headers=headers, name="NoneKey")

    # Check to see if the playbook repo exists before creating it
    print("---CHECKING FOR PLAYBOOK REPOSITORY")
    api = "/project/"+str(managementProjectID)+"/repositories"

    repositoryID = getIDFromName(s=s, url=host+api, headers=headers, name="Playbooks")

    if repositoryID == None:

        # Create the playbook repo
        print("---CREATING PLAYBOOK REPOSITORY")
        data = '{"name": "Playbooks", ' +                             \
               '"project_id": ' + str(managementProjectID) + ', ' +   \
               '"git_url": "' + str(playbookRepositoryUrl) + '", ' +  \
               '"ssh_key_id": ' + str(repositoryKeyID) + '}'

        response = s.post(url=host+api, headers=headers, data=data)
        checkStatus(response)

        # Get the ID of the new playbook repository
        repositoryID = getIDFromName(s=s, url=host+api, headers=headers, name="Playbooks")

    # Check to see if the vCenter inventory exists before creating it
    print("---CHECKING FOR VCENTER INVENTORY")
    api = "/project/"+str(managementProjectID)+"/inventory"

    inventoryID = getIDFromName(s=s, url=host+api, headers=headers, name="vCenter")

    if inventoryID == None:

        # Create the vCenter inventory
        print("---CREATING VCENTER INVENTORY")
        data = '{"name": "vCenter", ' +                              \
               '"project_id": ' + str(managementProjectID) + ', ' +  \
               '"inventory": "' + inventoryFilePath  + '", ' +       \
               '"key_id": ' + str(repositoryKeyID) + ', ' +          \
               '"ssh_key_id": ' + str(repositoryKeyID) + ', ' +      \
               '"type": "file"}'
        response = s.post(url=host+api, headers=headers, data=data)
        checkStatus(response)

        # Get the ID of the new vCenter inventory
        inventoryID = getIDFromName(s=s, url=host+api, headers=headers, name="vCenter")

    # Check to see if the blank environment exists before creating it
    print("---CHECKING FOR ENVIRONMENT")
    api = "/project/"+str(managementProjectID)+"/environment"

    environmentID = getIDFromName(s=s, url=host+api, headers=headers, name="EmptyEnvironment")

    if environmentID == None:
        print("---CREATING ENVIRONMENT")
        data = '{"name": "EmptyEnvironment", ' +                     \
               '"project_id": ' + str(managementProjectID) + ', ' +  \
               '"json": "{}"} '
        response = s.post(url=host+api, headers=headers, data=data)
        checkStatus(response)

        environmentID = getIDFromName(s=s, url=host+api, headers=headers, name="EmptyEnvironment")

    print("---CHECKING FOR ENVIRONMENT")
    api = "/project/"+str(managementProjectID)+"/environment"


    # If a token was generated at the start, clean it out
    print("---CLEANING ANY GENERATED TOKENS")
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
