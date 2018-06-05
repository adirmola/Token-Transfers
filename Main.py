# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 07:59:35 2018
@author: adirmola@gmail.com
"""

'''
this is the main procedure of the process of retreving token transfers of specific contract
the process asumes that you have mysql installed and running and that you have a database called 'ethereum_accounts'
'''

#Enter Token Name and Address to retrieve data from
'user parmeters'
tokenName="SomeToken" #only use for creatin uniq table on mysql
address="SomeAddress" #the contract address
#example
#tokenName="SRN_3_12_2017"
#address="0x68d57c9a1c35f63e2c83ee8e49a64e9d70528d25"

#scrap token transfers from ether scan
'status - currently working'
import etherscan_scrap_token_transfers
trxnsListTable=etherscan_scrap_token_transfers.scrapTokenTransfers(tokenName,address)

#scrap token holders from ether scan
'status - currently partial working as for etherscan limit the access to 1000 token holders'
import etherscan_scrap_getTokenHolders
etherscan_scrap_getTokenHolders.scrapTokenHolders(tokenName,address)

#scrap from etherscan full data of transaction that was scrap with "etherscan_scrap_token_transfers"
'status - currently not working properly as for etherscan update the transactions pages'
import etherscan_scrap_getTxData
etherscan_scrap_getTxData.getTrxData(tokenName,trxnsListTable)

##api get from etherplorer full data of transaction that was scrap with "etherscan_scrap_token_transfers"
#import ethplorer_api_getTxData_withoutProxy 
'status - unknown - not check lately'
#ethplorer_api_getTxData_withoutProxy.getTrxData_ethplorerApi(tokenName,trxnsListTable)


