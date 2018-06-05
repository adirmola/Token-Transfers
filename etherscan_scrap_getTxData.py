# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 16:55:54 2018

@author: adirmola@gmail.com
"""


#import relevant packages
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import gmtime, strftime
import time

def getTrxData(tokenName,trxnsListTable):
    """
    This method built to scrap full data of the transctions list - currentlly tnxns list from "etherscan_scrap_token_transfers"

    @param tokenName: the token name
    @param trxnsListTable: the name of table in mysql that hold the transaction hases list
    @return: transaction data saved on mysql
    """
    #capture begin time
    begin_time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
    #Name of the table that will create and store the data
    sqlTableName=tokenName+"_fullTxData"+"_eteherscan"
    
    #establish mysql connection
    cnx = mysql.connector.connect(user="root",password="root", port=3306, database="ethereum_accounts")
    cur = cnx.cursor(buffered=True)
    
    #initial quries to create table
    sqlQuery="Drop table IF EXISTS `" + sqlTableName + "`";
    cur.execute(sqlQuery)
    cnx.commit()
    sqlQuery="""CREATE TABLE `""" + sqlTableName + """` (
              `TxHash` longtext,
              `TxReceipt_Status` longtext,
              `Block_Height` REAL,
              `TimeStamp` longtext,
              `From` longtext,
              `To` longtext,
              `Token_Transfer` longtext,
              `Value` REAL,
              `Gas_Limit` REAL,
              `Gas_Used_By_Txn` REAL,
              `Gas_Price` REAL,
              `Actual_Tx_CostOrFee` REAL,
              `Nonce` REAL,
              `Input_Data` longtext
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
    
    #configure chrome webdriver
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors") #as sound
    chrome_options.add_argument("--disable-infobars") #disable aoutomate control massage bar
    chrome_options.add_argument("--incognito") #start incognito mode te get clean browser state
    chrome_options.add_experimental_option("useAutomationExtension", False) #disable loading extenssions
    #starting webdriver
    browser = webdriver.Chrome(chrome_options=chrome_options,executable_path=dir_path+'chromedriver.exe')
    #loop through all trnxns
    for x in range(0,numTx):
            txHash=txHashList[x][0] #get current txn hash
            while True: #loop untill no error
                url = "https://etherscan.io/tx/" + txHash #url build
                browser.get(url) #navigate to url
                if x==0:
                    time.sleep(8)
                try: #checking if element exist
                    txData=browser.find_element_by_id("ContentPlaceHolder1_maintable") 
                except: #if error accured so basically should do nothig but try again. 
                    #cleaning the coockies just in case
                    browser.delete_all_cookies
                else: #if there ws NO eroor so break error loop and continue on
                    break 
            #get arrays of headers and values html elements
            headers=txData.find_elements_by_xpath("(//div[contains(@class,'col-sm-3')])")
            values=txData.find_elements_by_xpath("(//div[contains(@class,'col-sm-9')])")
            
            fieldsListStr="" #variable for creating the string of fields for the insert query
            for i in range(0,14):
                if i<13:
                    fieldsListStr=fieldsListStr+"`"+headers[i].get_attribute('innerText').replace(":","").replace(" ","_").replace("/","Or")+"`,"
                else:
                    fieldsListStr=fieldsListStr+"`"+headers[i].get_attribute('innerText').replace(":","").replace(" ","_").replace("/","Or")+"`"
            
            valuesArr=[] #varaiable to create an array of values (non html) after manipulate where needed
            #TxHash
            valuesArr.append(values[0].get_attribute('innerText'))
            #TxReceipt Status
            valuesArr.append(values[1].get_attribute('innerText'))
            #Block Height
            valuesArr.append(float(values[2].get_attribute('innerText').split(" (")[0])) #removing the text part and coverting to num
            #TimeStamp
            valuesArr.append(values[3].get_attribute('innerText').split(" (")[1].replace(")","")) #removing the time past part
            #From
            valuesArr.append(values[4].get_attribute('innerText'))
            #To 
            valuesArr.append(values[5].get_attribute('innerText'))
            #Token Transfer- need to take care
            valuesArr.append(values[6].get_attribute('innerText'))
            #Value
            valuesArr.append(float(values[7].get_attribute('innerText').split(" Ether")[0])) #removing the text part and coverting to num
            #Gas Limit
            valuesArr.append(float(values[8].get_attribute('innerText')))
            #Gas Used By Txn
            valuesArr.append(float(values[9].get_attribute('innerText')))
            #Gas Price
            valuesArr.append(float(values[10].get_attribute('innerText').split(" Ether")[0])) #removing the text part and coverting to num
            #Actual Tx Cost/Fee
            valuesArr.append(float(values[11].get_attribute('innerText').split(" Ether")[0])) #removing the text part and coverting to num
            #Nonce
            valuesArr.append(float(values[12].get_attribute('innerText').split(" (")[0])) #removing the text part and coverting to num
            #Input Data
            valuesArr.append(values[13].find_element_by_id("inputdata").get_attribute("value")) 
            
            #running insert query
            insert = "INSERT INTO " + sqlTableName +  " (" + fieldsListStr + ") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(insert, (valuesArr))
            cnx.commit()
            
            #reset relevant vars
            del headers[:]
            del values[:]
            del valuesArr[:]
    
    
    cnx.close
    browser.close()
    browser.quit()
    print(begin_time)
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    
        
        
        
        
