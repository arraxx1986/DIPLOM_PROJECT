import time
import os
import pandas as pd
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import xlsxwriter

options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory":f"{os.getcwd()}"
}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(20)
driver.get('https://www.way2drug.com/antibac/')
time.sleep(5)
driver.find_element(By.XPATH, '//input[@id="SmilesField"]').send_keys('CC(C)N1CCC(CC1)NC2=NC(=NC3=CC(=C(C=C32)OC)OCCCN4CCCC4)C5CCCCC5')
driver.find_element(By.XPATH, '//button[@id="btn-sbmtTxtMol"]').click()
time.sleep(5)
driver.find_element(By.className("dt-button buttons-csv buttons-html5")).click()
time.sleep(5)

