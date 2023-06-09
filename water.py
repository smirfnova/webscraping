

import bs4
import urllib
#import requests
from bs4 import BeautifulSoup as soup



#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import datetime
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import ElementNotInteractableException
import time
import os

from joblib import Parallel, delayed
from multiprocessing import Pool
import threading

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

import zipfile
from datetime import date

#list of all state names
text = {
    "Goa",
    "A & N Islands",
    "D&NH and D&D",
    "Haryana",
    "Gujarat",
    "Puducherry",
    "Punjab",
    "Telangana",
    "Himachal Pradesh",
    "Bihar",
    "Mizoram",
    "Sikkim",
    "Arunachal Pradesh",

    "Uttarakhand",
    "Manipur",
    "Maharashtra",
    "Ladakh",
    "Andhra Pradesh",
    "Karnataka",
    "Nagaland",
   "Tamil Nadu",
    "Tripura",
    "Jammu & Kashmir",
    "Odisha",
    "Meghalaya",
    "Assam",
    "Madhya Pradesh",
    "Kerala",
    "Chhattisgarh",
    "Uttar Pradesh",
    "Rajasthan",
    "Jharkhand",
    "West Bengal",
    "Lakshadweep"
}
file_name = "info3.csv"
f = open(file_name, "w")

for t in text:
    print(t)
    driver = webdriver.Chrome('/Users/ladyjane/Desktop/script/chromedriver1')
    url = "https://ejalshakti.gov.in/jjmreport/JJMIndia.aspx"
    driver.get(url)
    search = "//*[text()= '" + t + "']"
    WebDriverWait(driver, 3000).until(EC.presence_of_element_located((By.XPATH, search)))
    time.sleep(1)
    

    states = driver.find_elements("xpath", search)
    test = False
    for state in states: #iterate through state elements until find a successful click
        try:
            state.click()
            test=True
        except ElementNotInteractableException:
            print("caught error")
        if test:
            break
    
    WebDriverWait(driver, 3000).until(EC.presence_of_element_located((By.ID, "tblBody")))
    time.sleep(6)
    page_soup = soup(driver.page_source, 'html.parser')
    table = page_soup.find("tbody", {"id": "tblBody"})
    table_elem = driver.find_element("id", "tblBody")
    ActionChains(driver).move_to_element(table_elem)

    table2 = page_soup.find("tbody", {"id": "tblBody_HGJ"})
    rows2 = table2.find_all("tr")
    rows = table.find_all("tr")
    write = ""
    dict1 = dict()
    for enum, row in enumerate(rows):
        cells = row.find_all("td")
        district = cells[0].find_all("div")[-1].text
        dict1[district] = []
        lst = []
        for enum, cell in enumerate(cells):
            if enum > 0 and enum < len(cells) - 2:
                divs = cell.find_all("div")
                text = divs[-1].text
                lst.append(str(text)) 
        dict1[district] = lst
    for enum, row in enumerate(rows2): #searching through table 2
        cells2 = row.find_all("td")
        district = cells2[0].find_all("div")[-1].text
        print(district)
        lst2 = []
        for enum, cell in enumerate(cells2):
            if enum > 0 and enum < len(cells) - 2:
                divs = cell.find_all("div")
                text = divs[-1].text
                lst2.append(str(text))
        print(lst2)
        d = date.today().strftime('%m/%d/%Y') 
        lst2.append(d)
        lst1 = dict1[district]
        lst3 = lst1 + lst2
        dict1[district] = lst3
        
    print(dict1)
    write = ""
    print(write)
    for key in dict1:
        lst = dict1[key]
        write = t + "," + key + ","
        for elem in lst:
            write = write + "\"" + elem + "\"" + ","
        write = write + "\n"
        f.write(write)  
        
f.close()

