# Local Compose Deployment

1. docker-compose up

2. docker-compose down


# Compose Deployment on Azure

1. login azure: docker login azure / az login

2. create resource group: az group create --name myResourceGroup --location westeurope

3. create aci context: docker context create aci acicontext

3b. use aci context: docker context use acicontext

4. create container registry: az acr create --resource-group myResourceGroup --name myContainerRegistry --sku Basic

5. log into container registry: az acr login --name myContainerRegistry

6. tag local image: docker tag cloudapp:latest loginserver.azurecr.io/cloudapp:latest
(docker context use default)

7. push image: docker push loginserver.azurecr.io/cloudapp:latest

8. use aci context: docker context use acicontext

8b. adapt docker-compose file with acr name

9. compose up: docker compose --file docker-compose-azure.yml up

10. clean up resources: az group delete --name myResourceGroup --yes --no-wait

## Alternative Container Registry: DockerHub

1. Tag image: docker tag cloudapp:latest <username>/cloudapp:latest
2. Push image: docker push <username>/cloudapp:latest
3. Change k8s deployment to fetch correct image