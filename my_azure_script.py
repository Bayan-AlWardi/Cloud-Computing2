from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient

def create_or_update_resource_group():
    # Define your Azure subscription ID and resource group name
    subscription_id = "82df11b8-d798-4bf1-8403-547465963129"
    resource_group_name = "lab4"
    location = "westeurope"  

    # Create a DefaultAzureCredential
    credential = DefaultAzureCredential()

    # Create a ResourceManagementClient instance
    client = ResourceManagementClient(credential, subscription_id)

    # Define the resource group parameters
    parameters = {"location": location}

    # Create or update the resource group
    result = client.resource_groups.create_or_update(resource_group_name, parameters)
    print(f"Resource group creation/update status: {result}\n\n")

def create_virtual_network():
    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="82df11b8-d798-4bf1-8403-547465963129",
    )

    response = client.virtual_networks.begin_create_or_update(
        resource_group_name="lab4",
        virtual_network_name="net5",
        parameters={
            "location": "westeurope",
            "properties": {"addressSpace": {"addressPrefixes": ["10.0.0.0/16"]}, "flowTimeoutInMinutes": 10},
        },
    ).result()
    print(f"Sucessfully created virtual network: {response}\n\n")

def create_subnet():
    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="82df11b8-d798-4bf1-8403-547465963129",
    )

    response = client.subnets.begin_create_or_update(
        resource_group_name="lab4",
        virtual_network_name="net5",
        subnet_name="snet5",
        subnet_parameters={"properties": {"addressPrefix": "10.0.0.0/16"}},
    ).result()
    print(f"Sucessfully created subnet {response}\n\n")

def create_public_ip_address():
    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="82df11b8-d798-4bf1-8403-547465963129",
    )

    response = client.public_ip_addresses.begin_create_or_update(
        resource_group_name="lab4",
        public_ip_address_name="ip5",
        parameters={"location": "westeurope"},
    ).result()
    print(f"Sucessfully created IP address {response}\n\n")

def create_network_interface():
    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="82df11b8-d798-4bf1-8403-547465963129",
    )

    try:
        response = client.network_interfaces.begin_create_or_update(
            resource_group_name="lab4",
            network_interface_name="nic5",
            parameters={
                "location": "westeurope",
                "properties": {
                    #"disableTcpStateTracking": True,
                    "enableAcceleratedNetworking": True,
                    "ipConfigurations": [
                        {
                            "name": "ip5",
                            "properties": {
                                "publicIPAddress": {
                                    "id": "/subscriptions/82df11b8-d798-4bf1-8403-547465963129/resourceGroups/lab4/providers/Microsoft.Network/publicIPAddresses/ip5"
                                },
                                "subnet": {
                                    "id": "/subscriptions/82df11b8-d798-4bf1-8403-547465963129/resourceGroups/lab4/providers/Microsoft.Network/virtualNetworks/net5/subnets/snet5"
                                },
                            },
                        }
                    ],
                },
            },
        ).result()
        print(f"Sucessfully created network interface: {response}\n\n")
    except Exception as e:
        print(f"Error creating network interface: {e}")

def create_virtual_machine():
    # Define your Azure subscription ID and resource group name
    subscription_id = "82df11b8-d798-4bf1-8403-547465963129"
    resource_group_name = "lab4"
    location = "westeurope"  # Replace with the desired location

    # Create a DefaultAzureCredential
    credential = DefaultAzureCredential()

    # Create ComputeManagementClient and NetworkManagementClient instances
    compute_client = ComputeManagementClient(credential, subscription_id)
    network_client = NetworkManagementClient(credential, subscription_id)

    # Define VM configuration
    vm_name = "vm5"
    admin_username = "bayanalwardi"
    ssh_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCtMO3CZ7FKH52k0JFC0D2F6xl4nqpPehaGbXTTS/rb3wB8DBY5M9hI6WXFdQa7C1Nd02EszR9mpAooMwphJoo/tmZLjYYxhKVI42RZIVPghQC8G3IxWJ4oPJ9fZ3DOEIgVNH5pZ8t/mEUkyJpxCkSQpEIpNKsDZ5zynI3pHur5KGsKDRvQIbBS55g9B47Wtn4QME87HxmFMfRxF2ljARJQiiqaLuOByzgcW9NMIzyVU6KlOH4ndAZFOaKVBbaGYhkyP1HVkLPOtlrQvzR4WdruW15Fhce5mh29418Y5aHlgR+U+oJh9RBHHb9jERSyO/rjVWSwlBzlgqc4I8JIM24evkRHtnqDKWQVxTI+O8EGzgU/NfoX6Ccay8bYikOBB076fyoIYzEdzIx3zA1nkh49ULPLdv1pQM3hjMbhvxM0+f3g8fRN6EJwRD+vTC+UPM599DzUlvUAMY3Reug0WF8XejyYM5RljiPLmEd3+iGWAdUmUs4MEjGogYc78Ara17s= bayanalwardi@Bayans-MacBook-Pro.local"
    vm_size = "Standard_D1_v2"

    # Define the virtual machine properties
    vm_properties = {
        "location": location,
        "osProfile": {
            "adminUsername": admin_username,
            "secrets": [],
            "computerName": vm_name,
            "linuxConfiguration": {
                "ssh": {
                    "publicKeys": [
                        {
                            "path": "/home/bayanalwardi/.ssh/authorized_keys",
                            "keyData": ssh_public_key
                        }
                    ]
                },
                "disablePasswordAuthentication": True
            }
        },
        "networkProfile": {
            "networkInterfaces": [
                {
                    "id": f"/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/networkInterfaces/nic5",
                    "properties": {
                        "primary": True
                    }
                }
            ]
        },
        "storageProfile": {
            "imageReference": {
                "sku": "16.04-LTS",
                "publisher": "Canonical",
                "version": "latest",
                "offer": "UbuntuServer"
            },
            "dataDisks": []
        },
        "hardwareProfile": {
            "vmSize": vm_size
        },
        "provisioningState": "Creating"
    }

    # Create the virtual machine
    vm = compute_client.virtual_machines.begin_create_or_update(
        resource_group_name, vm_name, vm_properties)
    vm.wait()
    print("Successfully created VM!\n")
    print(vm.result())


if __name__ == "__main__":
    create_or_update_resource_group()
    create_virtual_network()
    create_subnet()
    create_public_ip_address()
    create_network_interface()
    create_virtual_machine()