# openai-agents-fastapi

![architecture](.img/architecture.png)

This repo demonstrates a simple Python FastAPI application that uses several agents. It creates several agents (using the `autogen` framework) that each have their own functions to retrieve relevant data and the instructions needed to process that data.

### Physical Architecture

![physical-architecture](.img/physical-architecture.png)

## Disclaimer

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.**

## Prerequisites

- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- Azure subscription & resource group
- [Python 3.12](https://www.python.org/downloads/release/python-3123/)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd?tabs=winget-windows%2Cbrew-mac%2Cscript-linux&pivots=os-windows)
- [Terraform CLI](https://developer.hashicorp.com/terraform/tutorials/azure-get-started/install-cli)
- [Docker](https://docs.docker.com/engine/install/)

## Local Deployment

1.	**Remove (not just comment out, *remove*)** the following lines from the `infra/provider.tf` file. This is to prevent `azd` from trying to use a remote Terraform backend.

	```hcl
	backend "azurerm" {
	}
	```

1.	**Remove (not just comment out, *remove*)** the following lines from the `azure.yaml` file. This is to prevent `azd` from trying to use a remote backend to store its internal state.

	```yaml
	state:
		remote:
			backend: AzureBlobStorage
			config:
			accountName: 
			containerName: openai-agents-fastapi
	```

1.	Run the Azure Developer CLI `init` command to set up the environment files. You will be prompted to set a environment name. This name will be used later.

	```shell
	azd auth login

	azd init
	```

1.  This repo assumes you already have a resource group to deploy into. Run the following command to add this environment variable. You can also toggle
	whether or not to enable public network access.

	```shell
	azd env set AZURE_RESOURCE_GROUP "rg-openai-agents-fastapi"
	azd env set PUBLIC_NETWORK_ACCESS_ENABLED "true"
	```

1.  Run the Azure Developer CLI `up` command to build, provision & deploy the application

	```shell
	azd up
	```

## Local debugging (PowerShell)

1.  Create a virtual environment for the Python to run in

	```powershell
	cd src/api

	python -m venv .venv
	```

1.  Activate the virtual environment

	```powershell
	./.venv/Scripts/activate
	```

1.  Install the requirements

	```powershell
	pip install -r ./requirements.txt
	```

1.  Create a `.env` file with the following values (specify your own values):

	```powershell
	AZURE_OPENAI_ENDPOINT=
	OPENAI_API_VERSION=2024-06-01
	OPENAI_MODEL_ID=
	OPENAI_MODEL_API_NAME="gpt-4o-2024-05-13"
	CLIENT_ID=
	CLIENT_SECRET=
	AUTHORITY=
	OPENAI_CLIENT_ID=
	APIM_SUBSCRIPTION_KEY=
	APPLICATION_INSIGHTS_CONNECTION_STRING=
	```

1.  Run the API

	```powershell
	python -m uvicorn app.main:app --reload --env-file .env --log-level debug
	```

	Alternatively, you can open this repo in VS Code and use the included `.vscode/launch.json` file to launch the app.

1.  Query the API endpoint (this will take a minute or two to return). Alternatively, use the `test.http` file in the root of the repository.

	```powershell
	$Parameters = @{ Uri = "http://localhost:8000/v1/test"; Method = "POST"; Headers = @{ "Content-Type"= "application/json" } }

	$Body = (@{ "test" = ""; }) | ConvertTo-Json

	Invoke-WebRequest @Parameters -Body $Body | Select-Object Content | Format-Table -Wrap
	```

1.  The output will be the thread history (sorted by timestamp descending)

	```json
	{
			"test": ,
			"overall_result": "",
			"chat_results": [
				{
					"summary": "",
					"usage_including_cached_inference": {
						"prompt_tokens": ,
						"completion_tokens": ,
						"total_tokens": 
					},
					"usage_excluding_cached_inference": {
						"prompt_tokens": ,
						"completion_tokens": ,
						"total_tokens": 
					}
				}
	    ]
	}
	```

## Running in Azure

This demo will run the same API in Azure after the `azd up` command has finished building the Docker image, deploying the infrastructure & then deploying the application. In order for the application to run correctly, you will need to upload the data files to Azure Storage (the `/data` File Share) so they can be mounted as files on the Container App Docker container. Check the names of the environment variables of the Container App and ensure you have the same file names.

## Links
