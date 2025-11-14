Azure Microservices DevOps Project – End-to-End Deployment on AKS

This project demonstrates a fully automated Azure-native microservices deployment using:

Azure Kubernetes Service (AKS)

Azure Container Registry (ACR)

Terraform (IaC)

Azure DevOps Pipelines (CI/CD)

RBAC + Key Vault

Monitoring (Azure Monitor, Logs, Metrics)

Ingress Controller

User + Order Microservices

This README provides architecture, setup, commands, CI/CD flow, monitoring, screenshots, and repository structure for academic submission or professional documentation.

📌 1. Architecture Diagram

Located in: diagrams/architecture-diagram.png

Summary

User & Order microservices → Docker images → pushed to ACR.

Deployed on AKS using Kubernetes manifests.

Ingress Controller (NGINX) exposes /users and /orders routes.

Terraform provisions AKS, ACR, VNet, Subnets.

RBAC restricts user access (Developer, Operator, Admin).

Key Vault stores secrets such as DB credentials.

Azure DevOps Pipelines build → push → deploy.

Azure Monitor / Log Analytics used for metrics & logs.

📦 2. Repository Structure
azure-microservices-devops/
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── provider.tf
│
├── microservices/
│   ├── user-service/
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── order-service/
│       ├── main.py
│       ├── Dockerfile
│       └── requirements.txt
│
├── k8s-manifests/
│   ├── user-deployment.yaml
│   ├── user-service.yaml
│   ├── order-deployment.yaml
│   ├── order-service.yaml
│   └── ingress.yaml
│
├── diagrams/
│   └── architecture-diagram.png
│
├── azure-pipelines.yml
└── README.md

⚙️ 3. Infrastructure as Code (Terraform)

Terraform provisions:

✔ Resource Group
✔ Virtual Network + Subnets
✔ AKS Cluster
✔ ACR Registry
✔ Node Pool Settings
✔ RBAC Configuration
✔ System-assigned Managed Identity

Run Terraform:

cd terraform
terraform init
terraform plan
terraform apply -auto-approve


Outputs:

AKS kubeconfig

ACR login server

Node pool configuration

🔐 4. Security: RBAC + Key Vault
4.1 Role-Based Access Control (RBAC)

Roles created:

ClusterAdmin – full access

DevOpsUser – deploy apps only

ReadOnlyUser – logs/metrics only

Example command:

az role assignment create \
  --assignee <user-email> \
  --role "Azure Kubernetes Service Cluster User Role" \
  --scope $(az aks show -g rg -n aks --query id -o tsv)

4.2 Key Vault Integration

Secrets stored:

db-password

api-key

connection-string

Access granted to AKS:

az keyvault set-policy \
  --name my-keyvault \
  --spn <aks-msi-id> \
  --secret-permissions get list


Pods access secrets via CSI driver:

volumeMounts:
- name: secrets-store-inline
  mountPath: "/mnt/secrets"

🐳 5. Microservices
5.1 User Service

Python FastAPI

Endpoint: /users

Run locally:

uvicorn main:app --reload

5.2 Order Service

Python FastAPI

Endpoint: /orders

Run locally:

uvicorn main:app --reload

5.3 Docker Build
docker build -t user-service .
docker build -t order-service .

🚀 6. CI/CD Pipeline (Azure DevOps)

Pipeline file: azure-pipelines.yml

Stages
Stage 1: Build & Push
- task: Docker@2
  inputs:
    command: buildAndPush
    repository: $(ACR)/user-service

Stage 2: Deploy to AKS
- script: |
    kubectl apply -f k8s-manifests/

☸️ 7. Kubernetes Deployment
7.1 Deployments

user-deployment.yaml
order-deployment.yaml

7.2 Services

ClusterIP services expose microservices internally.

7.3 Ingress Controller

ingress.yaml contains:

- path: /users
  backend:
    service:
      name: user-service
      port:
        number: 8080

- path: /orders
  backend:
    service:
      name: order-service
      port:
        number: 8081

🌐 8. Exposed Endpoints

After LoadBalancer provisioning:

User Service:   http://<public-ip>/users
Order Service:  http://<public-ip>:81/orders
Ingress (optional): http://<public-ip>/user  and /order

📊 9. Monitoring & Logging

Enabled via:

Azure Monitor

Container Insights

Log Analytics Workspace

View metrics:

az monitor metrics list --resource <aks-id>


View logs:

kubectl logs <pod-name>

💰 10. Cost Optimization

Use Azure B4ms or A2 node size for student workloads

Enable Cluster Autoscaler

Use Spot Nodes (optional)

Store logs with retention (30 days)

🧪 11. Testing the Deployment
Test API endpoints:
curl http://<public-ip>/users
curl http://<public-ip>:81/orders

Check pods:
kubectl get pods -o wide

📷 12. Screenshots (Add into /screenshots folder)

Recommended screenshots:

AKS Cluster

ACR Images

Terraform Apply

Pipelines (Build + Deploy)

Running Pods

Curl Output for APIs

🏁 13. Conclusion

This project demonstrates:

✔ Fully automated microservices deployment
✔ Cloud-native architecture using AKS + ACR + Terraform
✔ Secure access with RBAC & Key Vault
✔ Production-grade setup with Ingress, Monitoring, CI/CD
✔ End-to-end DevOps implementation
