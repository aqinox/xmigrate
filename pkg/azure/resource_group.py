# Import the needed management objects from the libraries. The azure.common library
# is installed automatically with the other libraries.
from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import ResourceManagementClient
from utils.dbconn import *
from model.project import Project
import string, random

# Provision the resource group.
def create_rg(project):
    con = create_db_con()
    rg_location = Project.objects(name=project)[0]['location']
    rg_name =''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 8))
    rg_name = rg_name + "_xmigrate" 
    try:
        resource_client = get_client_from_cli_profile(ResourceManagementClient)
        print("Provisioning a resource group...some operations might take a minute or two.")
        rg_result = resource_client.resource_groups.create_or_update(
            rg_name, {"location": rg_location})
        print(
            "Provisioned resource group {rg_result.name} in the {rg_result.location} region")
        Project.objects(name=project).update(resoure_group=rg_result.name)
        return True
    except:
        return False
