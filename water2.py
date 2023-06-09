

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

#list on all state names 
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
    
    "Maharashtra",
    
    "Andhra Pradesh",
   "Karnataka",
    "Nagaland",
   
    "Tripura",
    
    "Odisha",
   "Meghalaya",
   "Assam",
 "Madhya Pradesh",
   
 "Chhattisgarh",
    "Uttar Pradesh",
    "Rajasthan",
    "Jharkhand",
    "West Bengal",
   "Lakshadweep"
 "Manipur",

  "Ladakh",
  "Tamil Nadu",
 "Jammu & Kashmir",
   "Kerala",
}
file_name = "info4.csv"
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
    for state in states: #keep trying to find the state element until successful
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
        print(district)
        search = "//a[text()='" + district + "']"


        districts = driver.find_elements("xpath", search)
        print(len(districts))
        districts[0].click()
        time.sleep(10)

        paths = driver.find_elements("xpath", ".//*[name()='svg']//*[name()='g']//*[name()='path']") 
        st = set()
        print(len(paths))
        for path in paths:
            try:
                ActionChains(driver).move_to_element(path).perform()
                page_soup = soup(driver.page_source, "html.parser")
                g = page_soup.find("g", {"class": "highcharts-label highcharts-tooltip highcharts-color-undefined"})
                text = g.find("text").text
                st.add(text)
            except:
                print(".")
        for elem in st:
            date = elem.split("upto ")[1].split(":")[0]
            water = elem.split(":")[1]
            write = t + "," + district + "," + date + "," + "\"" + water + "\"" + "\n"
            f.write(write)

        driver.back()
        time.sleep(20)

f.close()



