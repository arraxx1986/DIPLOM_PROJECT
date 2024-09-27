import time
import os
import pandas as pd
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


predicted = pd.read_excel('TOTAL_TARGETS_PREDICTED.xlsx')
list_predicted = predicted['targets'].tolist()
proved = pd.read_excel('TOTAL_TARGETS_PROVED.xlsx')
list_proved = proved['targets'].tolist()
list_total = []
list_total.extend(list_predicted)
list_total.extend(list_proved)
list_total = list(set(list_total))
l_t = pd.Series(list_total, name='targets')
l_t .to_excel('TARGETS_FOR_CALCULATION.xlsx')
os.remove('TOTAL_TARGETS_PREDICTED.xlsx')
os.remove('TOTAL_TARGETS_PROVED.xlsx')
df = pd.read_excel('TARGETS_FOR_CALCULATION.xlsx')
targets_list_calc = df['targets'].tolist()
targets_list_calc_str = ''
for i in targets_list_calc:
    targets_list_calc_str+= (' '+i)
print(targets_list_calc_str)

options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory":f"{os.getcwd()}"
}
options.add_experimental_option("prefs", prefs)
options.add_argument("start-maximized")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(20)
driver.get('http://bioinformatics.sdstate.edu/go/')
time.sleep(5)
driver.find_element(By.ID, "input_text").send_keys(targets_list_calc_str)
time.sleep(10)
driver.find_element(By.ID, "goButton").click()
time.sleep(2)
driver.find_element(By.ID,"selectGO-selectized").click()
time.sleep(3)
driver.find_element(By.XPATH, '(//div[@data-value="Disease.Alliance"])[1]').click()
time.sleep(3)
driver.find_element(By.XPATH, '(//li[@role="presentation"])[2]').click()
time.sleep(3)
driver.find_element(By.ID, "download_barplot-download_popup").click()
time.sleep(2)
driver.find_element(By.XPATH, '//a[@id="download_barplot-dl_pdf"]').click()
time.sleep(2)
os.rename('barplot.pdf.crdownload', 'barplot.pdf')