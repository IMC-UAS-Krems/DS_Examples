# Create an ASP.NET Core app in a Docker container from Docker Hub
# set -e # exit if error
# Variable block
let "randomIdentifier=$RANDOM*$RANDOM"
location="Canada Central"
resourceGroup="msdocs-app-service-rg-$randomIdentifier"
tag="deploy-linux-docker-app-only.sh"
appServicePlan="msdocs-app-service-plan-$randomIdentifier"
webapp="imc-ds-$randomIdentifier"

# Create a resource group.
echo "Creating $resourceGroup in "$location"..."
az group create --name $resourceGroup --location "$location" --tag $tag

# Create an App Service plan in S1 tier
echo "Creating $appServicePlan"
az appservice plan create --name $appServicePlan --resource-group $resourceGroup --sku F1 --is-linux

# Create a web app. To see list of available runtimes, run 'az webapp list-runtimes --linux'
echo "Creating $webapp"
az webapp create --name $webapp --resource-group $resourceGroup --plan $appServicePlan  --multicontainer-config-type compose --multicontainer-config-file /root/cloudapp/docker-compose-azure.yml

# Copy the result of the following command into a browser to see the static HTML site.
site="https://$webapp.azurewebsites.net/info"
echo $site
curl "$site"
