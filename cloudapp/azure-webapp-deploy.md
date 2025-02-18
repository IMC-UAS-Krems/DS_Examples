# Creating an Azure Webapp from a Docker container

We will now deploy our example cloudapp using Azure App services based on docker-compose.

## Method #1: Using the UI

- In the Azure UI (https://portal.azure.com), navigate to "Create a resource" -> "App services"
- Using the wizard, create a new resource group in the "Central US" region.
- Choose a unique name for the webapp. For instance `cloudapp-ds-imckrems`. The URL for you app will be then https://cloudapp-ds-imckrems.azurewebsites.net
- Change the SKU and size parameter to "Free F1"
- Provide the `docker-compose-azure.yml` file as input in the "Deployment" page.
- Go through the next steps leaving the default values.
- Wait until deployment is complete.
- The app can now be accessed using the previous address (https://cloudapp-ds-imckrems.azurewebsites.net/info)

## Method #2: Using the command line

(CLI samples from https://docs.microsoft.com/en-us/azure/app-service/samples-cli)

- Open a new terminal
- (PowerShell) Run the Azure CLI on a Docker container `` docker run -it -v ${PWD}/cloudapp:/root/cloudapp mcr.microsoft.com/azure-cli:2.9.0``
- Login into Azure using ``az login``
- Add execution permission for the Bash script ``chmod +x /root/cloudapp/deploy-linux-docker-cloudapp-only.sh``
- Execute the script ``./root/cloudapp/deploy-linux-docker-cloudapp-only.sh``
- Remove the resource group with ``az group delete --name <name-of-resource-group> --yes --no-wait``