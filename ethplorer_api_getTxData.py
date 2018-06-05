

import urllib.request as request
import json
import mysql.connector
from time import gmtime, strftime

def getTrxData_ethplorerApi(tokenName,trxnsListTable):
    """
    This method built to get data of the transctions list based on ethplorer.io api - currentlly tnxns list from 'etherscan_scrap_token_transfers'

    @param tokenName: the token name
    @param trxnsListTable: the name of table in mysql that hold the transaction hases list
    @return: transaction data saved on mysql
    """
    #capture begin time
    begin_time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
    #Name of the table that will create and store the data
    sqlTableName=tokenName+"_fullTxData_ethplorer"
    
    #establish mysql connection
    cnx = mysql.connector.connect(user="root",password="root", port=3306, database="ethereum_accounts")
    cur = cnx.cursor(buffered=True)
    
    #initial quries to create table
    sqlQuery="Drop table IF EXISTS `ethereum_accounts`.`" + sqlTableName + "`";
    cur.execute(sqlQuery)
    cnx.commit()
    sqlQuery="""CREATE TABLE `""" + sqlTableName + """` (
              `hash` longtext,
              `timestamp` longtext,
              `blockNumber` longtext,
              `confirmations` longtext,
              `success` longtext,
              `from` longtext,
              `to` longtext,
              `value` longtext,
              `input` longtext,
              `gasLimit` longtext,
              `gasUsed` longtext,
              `logs` longtext,
              `operations` longtext
               ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    cur.execute(sqlQuery)
    cnx.commit()
    
    #get uniq list of trnxns that was retrieve
    sqlQuery="SELECT DISTINCT TxHash FROM `ethereum_accounts`.`" + trxnsListTable + "`"
    cur.execute(sqlQuery)
    cnx.commit()
    txHashList=cur.fetchall()
    
    #get number of uniq trnxns
    numTx=len(txHashList)
    
    #loop through all trnxns
    for x in range(0,numTx):
        txHash=txHashList[x][0] #get current txn hash
        url = "https://api.ethplorer.io/getTxInfo/" + txHash + "?apiKey=freekey" #url build
        #json parsing
        api_req = request.urlopen(url) 
        api_res = api_req.read().decode('utf8')
        api_json_data=json.loads(api_res)
        
        #insert query
        try: #check if failing - happens when transaction didn't found
            insert = """INSERT INTO `""" + sqlTableName + """` 
                        (`hash`,
                         `timeStamp`,
                         `blockNumber`,
                         `confirmations`,
                         `success`,
                         `from`,
                         `to`,
                         `value`,
                         `input`,
                         `gasLimit`,
                         `gasUsed`,
                         `logs`,
                         `operations`) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            cur.execute(insert, (api_json_data["hash"],
                                 api_json_data["timestamp"],
                                 api_json_data["blockNumber"],
                                 api_json_data["confirmations"],
                                 api_json_data["success"],
                                 api_json_data["from"],
                                 api_json_data["to"],
                                 api_json_data["value"],
                                 api_json_data["input"],
                                 api_json_data["gasLimit"],
                                 api_json_data["gasUsed"],
                                 str(api_json_data["logs"]),
                                 str(api_json_data["operations"])
                                 )
                        )     
        except: #if trxnx didn't find marked it in the record
                insert = "INSERT INTO `" + sqlTableName + "`(`hash`,`timeStamp`) VALUES (%s,%s)"
                cur.execute(insert,(api_json_data["error"]["message"],"txnHash: " + txHash))
        cnx.commit()
                
    cnx.close
    print(begin_time)
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    
    
    
    
    ##error case
    #txHash=txHashList[1674][0]
    #url = "https://api.ethplorer.io/getTxInfo/" + txHash + "?apiKey=freekey"
    #print(url)
    #cnx.close