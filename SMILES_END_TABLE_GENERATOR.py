import time
import os
import pandas as pd
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def smiles_to_xlsx():
    with open('lotus_simple_search_result.sdf') as file:
        content = file.read()
    content = list(content.split(' '))
    smiles = []
    while '<SMILES>' in content:
            smiles.append(content[content.index('<SMILES>')+1])
            del content[content.index('<SMILES>')]
    smiles = [i[1:len(i)-3] for i in smiles]
    df = pd.DataFrame(smiles)
    df.to_excel('SMILES.xlsx')
    df = pd.read_excel('SMILES.xlsx')
    df2 = df.rename(columns={0: 'SMILES'})
    print(df2)
    df2.to_excel('SMILES_NEW.xlsx')
    os.remove('SMILES.xlsx')
    df = pd.read_excel('SMILES_NEW.xlsx')
    list_of_smiles = df['SMILES'].tolist()
    return list_of_smiles

def create_END_TABLE(list_of_smiles:list):
    names = []
    pathway = []
    superclass = []
    class_last = []
    options = webdriver.ChromeOptions()
    options.add_argument( "--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(20)
    driver.get('https://lotus.naturalproducts.net/')
    time.sleep(30)
    for i in list_of_smiles:
        time.sleep(3)
        driver.find_element(By.XPATH, '//input[@id="searchInput"]').send_keys(i)
        driver.find_element(By.XPATH, '//button[@id="searchButton"]').click()
        time.sleep(3)
        driver.find_element(By.XPATH, '//a[@class="cardItemHeadline card-link"]').click()
        time.sleep(3)
        try:
            t = driver.find_element(By.XPATH, '(//table[@class="table table-sm"]/tbody/tr//td)[2]').text
            names.append(t)
        except:
            names.append(0)
        try:
            d1 = driver.find_element(By.XPATH, '//td[@id = "npc1"]').text
            pathway.append(d1)
        except:
            pathway.append(0)
        try:
            d2 = driver.find_element(By.XPATH, '//td[@id = "npc2"]').text
            superclass.append(d2)
        except:
            superclass.append(0)
        try:
            d3 = driver.find_element(By.XPATH, '//td[@id = "npc3"]').text
            class_last.append(d3)
        except:
            class_last.append(0)
    df_table = pd.DataFrame(np.column_stack((list_of_smiles, names, pathway, superclass, class_last)), columns=['SMILES', 'name', 'pathway', 'superclass', 'class'])
    df_table.to_excel('END_TABLE.xlsx')
    os.remove('SMILES_NEW.xlsx')
    os.remove('lotus_simple_search_result.sdf')

def sdf_download(plant_name):
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory":f"{os.getcwd()}"
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument( "--window-size=1920,1080" )
    # options.page_load_strategy = 'eager'
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(30)
    driver.get('https://lotus.naturalproducts.net/')
    driver.find_element(By.XPATH, '//input[@id="searchInput"]').send_keys(plant_name)
    driver.find_element(By.XPATH, '//button[@id="searchButton"]').click()
    time.sleep(15)
    driver.find_element(By.ID, "downloadSDFfile").click()
    time.sleep(15)

plant_name = input('Введите латинское название растения: ')
flag = 0
try:
    sdf_download(plant_name)
except:
    flag = 1
if flag == 0:
    list_of_smiles = smiles_to_xlsx()
else:
    print('Для данного растения в базе данных отсутствуют известные вещества')
create_END_TABLE(list_of_smiles)



