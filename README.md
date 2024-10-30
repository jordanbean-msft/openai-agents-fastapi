# openai-agents-fastapi

![architecture](./.img/architecture.png)

## Disclaimer

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.**

## Prerequisites

- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- Azure subscription & resource group
- [Python 3.12](https://www.python.org/downloads/release/python-3123/)
- [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd?tabs=winget-windows%2Cbrew-mac%2Cscript-linux&pivots=os-windows)
- [Terraform CLI](https://developer.hashicorp.com/terraform/tutorials/azure-get-started/install-cli)
- [Docker](https://docs.docker.com/engine/install/)

## Deployment

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
    OPENAI_API_VERSION=2024-08-01-preview
    OPENAI_DEPLOYMENT_NAME=
    CLIENT_ID=
    CLIENT_SECRET=
    TENANT_ID=
    OPENAI_CLIENT_ID=
    APIM_SUBSCRIPTION_KEY=
    APPLICATION_INSIGHTS_CONNECTION_STRING=
    AZURE_OPENAI_API_KEY=
    USE_APIM=
	```

1.  Run the API

	```powershell
	python -m uvicorn app.main:app --reload --env-file .env --log-level debug
	```

	Alternatively, you can open this repo in VS Code and use the included `.vscode/launch.json` file to launch the app.

1.  Query the API endpoint (this will take a minute or two to return)

	```powershell
	$LoginParameters = @{ Uri = "http://localhost:8000/v1/analyze"; Method = "POST"; Headers = @{ "Content-Type"= "application/json" } }

	$Body = (@{ "stockTicker1": "MSFT", "companyName1": "Microsoft", "stockTicker2": "TSLA", "companyName2": "Tesla" }) | ConvertTo-Json

	Invoke-WebRequest @LoginParameters -Body $Body | Select-Object Content | Format-Table -Wrap
	```

1.  The output will look something like this.

    ```json
    {
        "stockTicker1": "MSFT",
        "companyName1": "Microsoft",
        "stockTicker2": "TSLA",
        "companyName2": "Tesla",
        "chat_results": [
            "### Stock Prices Analysis\n\n#### Microsoft (MSFT) Stock Prices:\n1. **2024-09-06:** \n   - Previous Close: $408.39\n   - Current Close: $401.7\n   - Change: -$6.69\n   \n2. **2024-09-09:** \n   - Previous Close: $401.7\n   - Current Close: $405.72\n   - Change: +$4.02\n   \n3. **2024-09-11:** \n   - Previous Close: $414.0\n   - Current Close: $423.04\n   - Change: +$9.04\n   \n#### Tesla (TSLA) Stock Prices:\n1. **2024-04-24:** \n   - Previous Close: $180.0\n   - Current Close: $203.4\n   - Change: +$23.4\n   \n2. **2024-09-11:** \n   - Previous Close: $216.27\n   - Current Close: $226.17\n   - Change: +$9.9\n   \n3. **2024-09-06:**\n   - Previous Close: $230.17\n   - Current Close: $240.73\n   - Change: +$10.56\n   \n### News Articles Analysis\n\n#### Microsoft (MSFT) News:\n1. **2024-09-06 - Goldman Sachs Analyst Insights:**\n   - Discussion on factors influencing the tech sector, including potential Federal Reserve rate cuts, the 2024 presidential election, and advancements in generative AI.\n   - Potential for increased volatility in tech stocks, including Microsoft.\n\n2. **2024-09-09 - Nvidia Sell-Off:**\n   - Analysts addressed the recent sell-off in Nvidia’s stock, indicating it was an exaggerated market reaction.\n   - The sentiment towards Nvidia influenced perceptions of other tech giants, including Microsoft.\n\n3. **2024-09-11 - Microsoft's Financial Performance:**\n   - Microsoft reported impressive revenue growth driven by its cloud services and AI initiatives.\n   - Positive market reaction due to its strong financial health and growth potential.\n\n#### Tesla (TSLA) News:\n1. **2024-04-24 - Tesla's Q1 Earnings Report:**\n   - Despite a decline in revenue and net income, the announcement of accelerating the launch of more affordable vehicles led to a surge in stock price.\n\n2. **2024-09-11 - Analysts Set New Price Targets:**\n   - Analysts set new optimistic price targets based on Tesla’s advancements in autonomous driving technology and market presence.\n\n3. **2024-09-06 - FSD Release for Europe and China:**\n   - Positive reception by investors due to the release of Full Self-Driving software for Europe and China, highlighting Tesla’s progress in autonomous driving technology.\n\n### Correlation Analysis\n\nIn analyzing the stock prices and news articles from both Microsoft and Tesla, the following observations can be made:\n\n- **Tech Sector Influence:** Both companies are significantly influenced by broader tech sector sentiments. For instance, discussions on generative AI and Federal Reserve rate cuts affect tech stocks like Microsoft. Similarly, advancements in technology, such as Tesla’s autonomous driving technology, drive investor optimism.\n\n- **Performance-Driven Responses:** Positive financial performance reports and strategic advancements (e.g., Microsoft's revenue growth, Tesla’s vehicle launch acceleration and FSD software release) result in positive stock price reactions for both companies.\n\n- **Investor Sentiment:** News articles often reflect market sentiment, which impacts stock prices. For example, optimistic targets set by analysts boost Tesla’s stock, while Microsoft's strong performance in cloud and AI is mirrored in its stock prices.\n\nWhile both companies operate in different segments (software/cloud services vs. electric vehicles/autonomous driving), they show a correlation in how broader tech sector developments and positive news concerning technological advancements and financial performance influence their stock prices. However, a direct correlation between their stock prices may not be evident from this short observation period alone, requiring a more extended data set for a robust conclusion.",
            "Overall, while both Microsoft and Tesla show independent movements in their stock prices based on company-specific news and performance, there are broader market trends and sector-wide influences that simultaneously affect them. The advancements in technology and investor sentiment driven by optimistic targets or significant product releases can create correlated movements in tech stocks generally, even though the specifics of their industries differ. Therefore, while direct correlation from brief data isn’t strong, certain tech sector factors can create a synchronous impact on both Microsoft and Tesla stock prices."
        ]
    }
    ```

## Links
