#!/usr/bin/env python3
import requests
import json
import time
import getpass
import pprint
import subprocess

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
        pprint.pprint(vars(response))
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

def createTaskTemplate(
    s, host, headers,
    templateName, playbookPath,
    projectID, repositoryID, repositoryKeyID,
    inventoryID, environmentID):

    print("---CHECKING FOR TEMPLATE: " + templateName)
    api = "/project/" + str(projectID) + "/templates"
    response = s.get(url=host+api, headers=headers)
    checkStatus(response)

    # Check to see if the template exists
    templates = json.loads(response.text)
    for template in templates:
        if template["alias"] == templateName:
            print("Found template: " + templateName + " with ID: " + str(template["id"]))
            return template["id"]

    # Create the template if it does not exist
    print("---CREATING TEMPLATE: " + templateName)

    # Templates expect an empty dict for arguments, not null, represented by two quotes ("")
    data = '{"ssh_key_id": ' + str(repositoryKeyID) +  ', ' +  \
           '"project_id": ' + str(projectID) + ', ' +          \
           '"inventory_id": ' + str(inventoryID) + ', ' +      \
           '"repository_id": ' + str(repositoryID) + ', ' +    \
           '"environment_id": ' + str(environmentID) + ', ' +  \
           '"alias": "' + templateName + '", ' +               \
           '"playbook": "' + playbookPath + '", ' +            \
           '"arguments": "[]", ' +                             \
           '"override_args": false}'

    response = s.post(url=host+api, headers=headers, data=data)
    checkStatus(response)

    # Retrieve templates ID
    response = s.get(url=host+api, headers=headers)
    checkStatus(response)

    templates = json.loads(response.text)
    for template in templates:
        if template["alias"] == templateName:
            "Created template: " + templateName + "with ID: " + str(template["id"])
            return template["id"]

    return templateID

def main():

    # Get the local machine IP assigned to the first adapter,
    #  this is usually the primary IP but may need to be changed

    ps = subprocess.Popen(('hostname', '-I'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('cut', '-d', ' ', '-f1'), stdin=ps.stdout)
    controlIP = (output.decode("utf-8").strip())

    ### CONFIGURATION ITEMS ###

    # The semaphore host URL
    host = "http://localhost:4000/api"

    # The URL for the git repo holding the playbooks
    playbookRepositoryUrl = "http://" + controlIP + ":3000/333TRS/rous.git"

    # Root folder for ansible configuration files in rous
    ansiblePathInRepository = "ansible/"

    # Root folder for terraform configuration files in rous
    terraformPathInRepository = "terraform/"

    # The relative path from the playbook repository to the inventory file
    #  This will usually just be the name of the inventory file if the
    #  if the inventory file sits in the root directory
    inventoryFilePath = ansiblePathInRepository + "vm.vmware.yml"

    # The relative path from the playbook repository to the directory
    #  that holds all of the playbooks
    playbooksDirPath = "ansible/"

    ### TOP LEVEL VARIABLES ###
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    s = requests.Session()
    sessionToken = ""
    updatedSessionToken = False

    managementProjectID = None
    repositoryID = None
    repositoryKeyID = None
    inventoryKeyID = None
    vcenterInventoryID = None
    localhostInventoryID = None
    environmentID = None


    api = "/auth/login"

    # Loop until the user can login
    while(True):
        print("---LOGINING IN")
        print("Please enter Semaphore admin credentials")

        user = input("Semaphore User: ")
        passwd = getpass.getpass(prompt="Password: ")
        data = '{"auth":"'+ user + '" , ' +          \
               '"password":"' + passwd + '"}'
        response = s.post(url=host+api, headers=headers, data=data)

        # If the code is a 401, we want to loop
        #    it it's not, checkStatus will could see success
        #    and continue, or a failure we don't wan to handle
        #    and end
        if response.status_code != 401:
            checkStatus(response)
            break

        print("Incorrect username or password")

     # Code to delete one off token-- useful if a token was generated
     #  and expected to be removed at the end,
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
        updatedSessionToken = True

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

    # Check to see if the key of type password login that does not have a password set
    #     exists bedore creating it
    print("---CHECKING FOR KEY ID OF TYPE LP")
    api = "/project/" + str(managementProjectID) + "/keys"

    inventoryKeyID = getIDFromName(s=s, url=host+api, headers=headers, name="NoneKeyLP")

    if inventoryKeyID == None:

        # Create the key
        print("---CREATING KEY OF TYPE LP")
        data = '{"name": "NoneKeyLP", ' +                                 \
               '"type": "login_password", ' +                             \
               '"login_password": {"login": "", "password": "none"}, ' +  \
               '"project_id": ' + str(managementProjectID) + '}'

        response = s.post(url=host+api, headers=headers, data=data)
        checkStatus(response)

        # Get the created key ID
        inventoryKeyID = getIDFromName(s=s, url=host+api, headers=headers, name="NoneKeyLP")

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

    vcenterInventoryID = getIDFromName(s=s, url=host+api, headers=headers, name="vCenter")

    if vcenterInventoryID == None:

        # Create the vCenter inventory
        print("---CREATING VCENTER INVENTORY")
        data = '{"name": "vCenter", ' +                              \
               '"project_id": ' + str(managementProjectID) + ', ' +  \
               '"inventory": "' + inventoryFilePath  + '", ' +       \
               '"key_id": ' + str(repositoryKeyID) + ', ' +          \
               '"ssh_key_id": ' + str(inventoryKeyID) + ', ' +       \
               '"type": "file"}'
        response = s.post(url=host+api, headers=headers, data=data)
        checkStatus(response)

        # Get the ID of the new vCenter inventory
        vcenterInventoryID = getIDFromName(s=s, url=host+api, headers=headers, name="vCenter")

    # Check to see if the localhost inventory exists before creating it
    print("---CHECKING FOR LOCALHOST INVENTORY")
    api = "/project/"+str(managementProjectID)+"/inventory"

    localhostInventoryID = getIDFromName(s=s, url=host+api, headers=headers, name="localhost")

    if localhostInventoryID == None:

        staticInventory = "[LOCALHOST]\\n" + controlIP

        # Create the localhost inventory
        print("---CREATING LOCALHOST INVENTORY")
        data = '{"name": "localhost", '                            + \
               '"project_id": ' + str(managementProjectID) + ', '  + \
               '"inventory": "' + staticInventory  + '", '         + \
               '"key_id": ' + str(repositoryKeyID) + ', '          + \
               '"ssh_key_id": ' + str(inventoryKeyID) + ', '       + \
               '"type": "static"}'
        response = s.post(url=host+api, headers=headers, data=data)
        checkStatus(response)

        # Get the ID of the new vCenter inventory
        localhostInventoryID = getIDFromName(s=s, url=host+api, headers=headers, name="localhost")

    # Check to see if the blank environment exists before creating it
    print("---CHECKING FOR ENVIRONMENT")
    api = "/project/"+str(managementProjectID)+"/environment"

    environmentID = getIDFromName(s=s, url=host+api, headers=headers, name="Env")

    env = '"{\\"api_key\\": \\"' + sessionToken + '\\",'                              + \
          '\\"controlIP\\": \\"192.168.100.1\\",'                                     + \
          '\\"playbookRepositoryURL\\": \\"' + playbookRepositoryUrl + '\\",'         + \
          '\\"ansiblePathInRepository\\": \\"' + ansiblePathInRepository + '\\",'     + \
          '\\"terraformPathInRepository\\": \\"' + terraformPathInRepository + '\\"'  + \
          '}"'
    print(env)

    if environmentID == None:
        print("---CREATING ENVIRONMENT")
        data = '{"name": "Env", ' +                                  \
               '"project_id": ' + str(managementProjectID) + ', ' +  \
               '"json": ' + env + '}'
        response = s.post(url=host+api, headers=headers, data=data)
        checkStatus(response)

        environmentID = getIDFromName(s=s, url=host+api, headers=headers, name="Env")

    if updatedSessionToken == True:
        api = "/project/" + str(managementProjectID) + "/environment/" + str(environmentID)
        print("---UPDATING TOKEN IN ENVIRONMENT")
        data = '{"json": ' + env + '}'
        response = s.put(url=host+api, headers=headers, data=data)

    # Create any task templates needed in the project
    # Parameters for convenience:

    # def createTaskTemplate(
    #       s, host, headers,
    #       templateName, playbookPath,
    #       projectID, repositoryID, repositoryKeyID,
    #       inventoryID, environmentID):

    # Task template for create class

    createTaskTemplate(
        s=s, host=host, headers=headers,
        templateName="Create Class", playbookPath=playbooksDirPath + "createClassInSemaphore.yml",
        projectID=managementProjectID, repositoryID=repositoryID, repositoryKeyID=repositoryKeyID,
        inventoryID=localhostInventoryID, environmentID=environmentID)

    createTaskTemplate(
        s=s, host=host, headers=headers,
        templateName="Get VM Info", playbookPath=playbooksDirPath + "get.vm.info.yml",
        projectID=managementProjectID, repositoryID=repositoryID, repositoryKeyID=repositoryKeyID,
        inventoryID=vcenterInventoryID, environmentID=environmentID)

    # Not currently cleaning token because the Create Class project needs
    # the token to call the api to create other projects

    # If a token was generated at the start, clean it out
    # print("---CLEANING ANY GENERATED TOKENS")
    # api = "/user/tokens"

    #if cleanSessionToken == True:
    #    print("Trying to clean")
    #    response = s.delete(url=host+api+'/'+sessionToken, headers=headers)
    #    checkStatus(response)
    #    print("Deleted: " + sessionToken)
    #else:
    #    print("No token to clean")

if __name__ == "__main__":
    main()
