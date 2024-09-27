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
driver.get('https://prediction.charite.de/subpages/target_prediction.php')
time.sleep(5)
df = pd.read_excel('END_TABLE_TOXICITY.xlsx')
list_of_smiles = df['SMILES'].tolist()
time.sleep(5)
targets = []
for i in list_of_smiles:
    try:
        driver.find_element(By.ID, "smiles_string").send_keys(i)
        time.sleep(5)
        driver.find_element(By.XPATH, '(//button[@class="btn btn-outline-secondary"])[2]').click()
        time.sleep(3)
        driver.find_element(By.XPATH, '//button[@name="searchtype"]').click()
        time.sleep(5)
        button_numbers = driver.find_elements(By.XPATH, '//button[@class="dt-button buttons-excel buttons-html5"]')
        if len(button_numbers) == 3:
            driver.find_element(By.XPATH, '(//button[@class="dt-button buttons-excel buttons-html5"])[2]').click()
            time.sleep(5)
            df = pd.read_excel('Targets.xlsx')
            df.drop([0], inplace=True)
            uniprot_id = []
            uniprot_id = df['Unnamed: 2'].tolist()
            targets.extend(uniprot_id)
            os.remove('Targets.xlsx')
        elif len(button_numbers) == 2:
            driver.find_element(By.XPATH, '(//button[@class="dt-button buttons-excel buttons-html5"])[1]').click()
            time.sleep(5)
            df = pd.read_excel('Targets.xlsx')
            df.drop([0], inplace=True)
            uniprot_id = []
            uniprot_id = df['Unnamed: 2'].tolist()
            targets.extend(uniprot_id)
            os.remove('Targets.xlsx')
        driver.get('https://prediction.charite.de/subpages/target_prediction.php')
        time.sleep(5)
    except:
        pass
targets_= list(set(targets))
a_ser = pd.Series(targets, name='targets')
a_ser.to_excel('TOTAL_TARGETS_PREDICTED.xlsx')