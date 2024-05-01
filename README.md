# FastAPI Project Setup in GitHub Codespaces

This README guides you through setting up and running the FastAPI project in GitHub Codespaces, including environment management, server operations, and Docker integration.

## Running the Project in GitHub Codespaces

### 1. Setup Codespace

- Open the GitHub repository in your browser.
- Click on the "Code" button, then select "Open with Codespaces" > "New codespace".

### 2. Environment Setup

Once your codespace is ready, set up a virtual environment and install dependencies:

```bash
# Create a virtual environment
python -m venv venv
```

```bash
# Activate the virtual environment
source venv/bin/activate
```

```bash
# Install requirements
pip install -r requirements.txt
```
### 3\. Run the Server

To run the FastAPI server on port 8000:


`uvicorn app:app --host 0.0.0.0 --port 8000 --reload`

### 4\. Port Forwarding

*   GitHub Codespaces will automatically suggest port forwarding for port 8000.
    
*   Set the port to "Public" to access the web server via the provided URL, typically formatted as:
    
    `https://port-8000-your-codespace-name.githubpreview.dev`
    

Testing the Server
------------------

Access the `/predict` endpoint using the following URL format:

`https://port-8000-your-codespace-name.githubpreview.dev/predict?text=Your%20example%20text%20here`

Replace `Your%20example%20text%20here` with the URL-encoded text you wish to analyze.

Docker Integration
------------------

### Building the Docker Image

Build the Docker image using:



`docker build -t myapi .`

Testing the Docker Container
------------------
```bash
docker run -d -p 8000:80 --name myapi myapi
```

### Docker Image Upload to Azure ACR

#### Prerequisites

Ensure Azure CLI is installed in your Codespace:



`pip install azure-cli`

Login to Azure:



`az login --use-device-code`

Login to your Azure Container Registry:



`az acr login --name <RegistryName>`

Tag and push the Docker image:



```
docker tag myapi <RegistryName>.azurecr.io/myapi:v1 
docker push <RegistryName>.azurecr.io/myapi:v1
```

Replace `<RegistryName>` with your actual Azure Container Registry name.

### Verifying the Image in ACR

List the repositories in your ACR to verify the upload:

`az acr repository list --name <RegistryName> --output table`

### Deploying Docker Image on Azure Container Instances (ACI)

After pushing your Docker image to Azure Container Registry (ACR), the next step is to deploy this image on Azure Container Instances (ACI) to run your application in the cloud.

#### Create an Azure Container Instance

Here’s how to deploy your Docker image from ACR to ACI:

1.  **Create a Container Instance using Azure CLI**: You will need to specify the image to use from your ACR, the CPU and memory requirements, and any other necessary configurations such as port and environment variables.

```
# Create the container instance
az container create \
  --resource-group <ResourceGroupName> \
  --name myfastapi \
  --image <RegistryName>.azurecr.io/myapi:v1 \
  --cpu 1 --memory 1 \
  --registry-login-server <RegistryName>.azurecr.io \
  --registry-username <ACRUsername> \
  --registry-password <ACRPassword> \
  --dns-name-label <myfastapi-dns-name-label> \
  --ports 80
```

*   Replace `<ResourceGroupName>` with your Azure Resource Group name.
*   `<RegistryName>`, `<ACRUsername>`, and `<ACRPassword>` should be replaced with your ACR details.
*   `<myfastapi-dns-name-label>` is a unique DNS name label for your container.

2.  **Configure DNS Name Label**: The DNS name label allows you to access your application via a user-friendly URL. It must be unique within the Azure region.

#### Accessing Your Application

Once the deployment is complete, you can access your FastAPI application through the fully qualified domain name (FQDN). The URL will be structured as follows:
```
http://<myfastapi-dns-name-label>.<region>.azurecontainer.io
```
Replace `<myfastapi-dns-name-label>` and `<region>` with your specific details.

#### Managing the Container Instance

To manage your container instance, you can use the following Azure CLI commands:

*   **Check the state of the container instance**:

    `az container show --resource-group <ResourceGroupName> --name myfastapi --query instanceView.state`
    
*   **View logs of the container instance**:

    `az container logs --resource-group <ResourceGroupName> --name myfastapi`
    
*   **Delete the container instance**:
    
    `az container delete --resource-group <ResourceGroupName> --name myfastapi`
