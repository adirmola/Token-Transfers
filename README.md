# Tokens-Transfers

The porpuse of this project is to retrieve Token transfers of specific contract from Ethereum blockchain and store them in Mysql for later analysis.

### The process include several parts:
1. Retrieve Tokens transfers of desired contract.
2. Retrieve full transaction data based on given list of transaction hashes (from two sources).
3. Retrieve Token holders of desired contract.

### Brief description of the moduls:
* Main.py	- proposed execution	
* etherscan_scrap_address_txs.py	- get all transaction of specific contract	
* etherscan_scrap_getTokenHolders.py	- get transaction holders of specific contract	
* etherscan_scrap_getTxData.py	- retrieve full data of transactions	
* etherscan_scrap_token_transfers.py	- retrieve token transfer of specific contract	
* ethplorer_api_getTxData.py	- get transaction data from another source

### Prerequisites
For running the script you need installed the following packages:
1. mysql
2. selenium
3. BeautifulSoup4
4. requests

You also need:
1. chromedriver.exe located in the main folder when you stored the project files.
2. mysql installed and running on you pc.
