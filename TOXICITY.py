import time
import os
import pandas as pd
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

df = pd.read_excel('END_TABLE.xlsx')
list_of_smiles = df['SMILES'].tolist()
total_list_of_targets = []
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory":f"{os.getcwd()}"
}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(20)
driver.get('https://tox.charite.de/protox3/')
driver.find_element(By.XPATH, '(//div[@id="ddtopmenubar"]//a[@target="_self"])[2]').click()
time.sleep(1)
predicted_LD50 = []
predicted_toxicity_class = []
average_similarity = []
prediction_accuracy = []
for i in list_of_smiles:
    try:
        driver.find_element(By.ID, "smiles_field").send_keys(i)
        time.sleep(3)
        driver.find_element(By.XPATH, '(//input[@type="submit"])[2]').click()
        time.sleep(3)
        driver.find_element(By.ID, "button_all").click()
        time.sleep(3)
        driver.find_element(By.ID, "start_pred").click()
        time.sleep(3)
    except:
        pass
    try:
        predicted_LD50.append(driver.find_element(By.XPATH, '//h1[@style="background:#f6faf3"]').text[16::])
        time.sleep(1)
    except:
        predicted_LD50.append(0)
    try:
        predicted_toxicity_class.append(driver.find_element(By.XPATH, '//h1[@style="background:#C8FE2E"]').text[26::])
        time.sleep(1)
    except:
        predicted_toxicity_class.append(0)
    try:
        average_similarity.append(driver.find_element(By.XPATH, '(//h1[@style="background:#9ff781"])[1]').text[20::])
        time.sleep(1)
    except:
        average_similarity.append(0)
    try:
        prediction_accuracy.append(driver.find_element(By.XPATH, '(//h1[@style="background:#9ff781"])[2]').text[21::])
        time.sleep(1)
    except:
        prediction_accuracy.append(0)
    driver.find_element(By.XPATH, '(//div[@id="ddtopmenubar"]//a[@target="_self"])[2]').click()
    time.sleep(1)
df = pd.read_excel('END_TABLE.xlsx')
SMILES = df['SMILES'].tolist()
name = df['name'].tolist()
pathway = df['pathway'].tolist()
superclass = df['superclass'].tolist()
class_col = df['class'].tolist()
df_table = pd.DataFrame(np.column_stack((SMILES, name, pathway, superclass, class_col, predicted_LD50, predicted_toxicity_class, average_similarity,prediction_accuracy)), columns=['SMILES', 'name', 'pathway', 'superclass', 'class', 'predicted_LD50', 'predicted_toxicity_class', 'average_similarity','prediction_accuracy'])
df_table.to_excel('END_TABLE_TOXICITY.xlsx')
os.remove('END_TABLE.xlsx')


