# Local k8s deployment

1. reset k8s cluster in docker-desktop

2. apply cloudapp deployment: kubectl apply -f deployment-cloudapp.yaml

3. apply redis deployment: kubectl apply -f deployment-redis.yaml

4. Access service at http://localhost:30001/info

5. kill a pod: kubectl delete pod <pod_id>

6. scale up deployment: kubectl scale deployment.v1.apps/cloudapp --replicas=6

7. delete deployments: kubectl delete -f deployment-cloudapp.yaml 


# Azure Kubernetes Service

1. az login

2. create resource group: az group create --name resourceGroup --location westeurope

3. create acr registry and tag image (see compose-deploy.md - no need for aci context)

4. create a new AKS cluster with 1 node: az aks create --resource-group resourceGroup --name myCluster --node-count 1 --generate-ssh-keys

5. attach acr to k8s cluster: az aks update -n myAKSCluster -g myResourceGroup --attach-acr <acr-name>

6. configure Kubernetes to use the cluster: az aks get-credentials --resource-group resourceGroup --name myCluster

7. check that current context is set to azure: kubectl config get-contexts

8. apply deployment: kubectl apply -f deployment-redis.yaml

9. clean up resources: az group delete --name myResourceGroup --yes --no-wait