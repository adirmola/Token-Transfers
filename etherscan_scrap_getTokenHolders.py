# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 12:02:41 2018
@author: adirmola@gmail.com
"""

#import relevant packages
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import gmtime, strftime
import time 

def scrapTokenHolders(tokenName,address):
    """
    This method built to retrieve token holders from etherscan.io 

    @param tokenName: the token name
    @param address: the address of contract to get token transfer
    @return: transaction data saved on mysql
    """
    #capture begin time
    begin_time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
    #set the beginig page (part of the url) to scrap. basically should not change unless for debuging or parallelel scrap
    page=1
    
    #Name of the table that will create and store the data
    sqlTableName=tokenName+"_token_holders_etherscan"
    
    #create connection with local mysql server
    cnx = mysql.connector.connect(user="root",password="root", port=3306, database="ethereum_accounts")
    cur = cnx.cursor()
    
    #initial quries to create table
    sqlQuery="Drop table IF EXISTS `ethereum_accounts`.`" + sqlTableName + "`";
    cur.execute(sqlQuery)
    cnx.commit()
    sqlQuery="""CREATE TABLE `""" + sqlTableName + """` (
        `Rank` varchar(20),
          `Address` varchar(64) DEFAULT NULL,
          `Quantity` longtext,
          `Percentage` varchar(10) DEFAULT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    cur.execute(sqlQuery)
    cnx.commit()
    
    #configure chrome webdriver
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors") #as sound
    chrome_options.add_argument("--disable-infobars") #disable aoutomate control massage bar
    chrome_options.add_argument("--incognito") #start incognito mode te get clean browser state
    chrome_options.add_experimental_option("useAutomationExtension", False) #disable loading extenssions
    #starting webdriver
    browser = webdriver.Chrome(chrome_options=chrome_options,executable_path=dir_path+'chromedriver.exe')
    #loop until breakpoint - break will occur when the string 'There are no matching entries' will found in page
    while True:
        while True: #loop untill error done - taking care for case that the website trying to limit uses
            #url build
            #https://etherscan.io/token/generic-tokenholders2?a=0x4162178b78d6985480a308b2190ee5517460406d&s=1.54070133359259E%2b27&p=
            url = "https://etherscan.io/token/generic-tokenholders2?a=" + address + "&s=1.54070133359259E%2b27&p=" + str(page)
            browser.get(url) #navigate to url
            if page==1:
                time.sleep(8)
            try: #checking if the page contain no table ellement - if no it's meaning the website blocking the script
                #get table html as text for further proccessing
                table=browser.find_element_by_tag_name("table").get_attribute('innerHTML')
            except: #if error accured so basically should do nothig but try again. 
                #cleaning the coockies just in case
                browser.delete_all_cookies
            else: #if there ws NO eroor so break error loop and continue on
                break
        #checking if data was end and break main loop
        if table.find("There are no matching entries")>0:
            break
        #converting html text to array
        table_data = [[cell.text for cell in row("td")]
                                 for row in BeautifulSoup(table,"lxml")("tr")]
        #insert all records to sql table
        for i in range(len(table_data)-1):
            insert = "INSERT INTO " + sqlTableName +  " (`Rank`,`Address`,`Quantity`,`Percentage`) VALUES (%s,%s,%s,%s)"
            cur.execute(insert, (table_data[i+1][0],table_data[i+1][1],table_data[i+1][2],table_data[i+1][3]))
            cnx.commit()
        del table_data[:]
        page+=1
    
    #end configur
    cnx.close #close connection to mysql
    browser.close()
    browser.quit()
    #print begin and end time
    print(begin_time)
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))


    
    
