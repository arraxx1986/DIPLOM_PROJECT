import time
import os
import pandas as pd
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import xlsxwriter

def web_driver():
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": f"{os.getcwd()}"
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(30)
    return driver

def sdf_download(plant_name, driver):
    driver.get('https://lotus.naturalproducts.net/')
    driver.find_element(By.XPATH, '//input[@id="searchInput"]').send_keys(plant_name)
    driver.find_element(By.XPATH, '//button[@id="searchButton"]').click()
    time.sleep(15)
    driver.find_element(By.ID, "downloadSDFfile").click()
    time.sleep(15)

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
    driver = web_driver()
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

def tagets_for_calculation():
    predicted = pd.read_excel('TOTAL_TARGETS_PREDICTED.xlsx')
    list_predicted = predicted['targets'].tolist()
    proved = pd.read_excel('TOTAL_TARGETS_PROVED.xlsx')
    list_proved = proved['targets'].tolist()
    list_total = []
    list_total.extend(list_predicted)
    list_total.extend(list_proved)
    list_total = list(set(list_total))
    l_t = pd.Series(list_total, name='targets')
    l_t.to_excel('TARGETS_FOR_CALCULATION.xlsx')
    os.remove('TOTAL_TARGETS_PREDICTED.xlsx')
    os.remove('TOTAL_TARGETS_PROVED.xlsx')
    df = pd.read_excel('TARGETS_FOR_CALCULATION.xlsx')
    targets_list_calc = df['targets'].tolist()
    targets_list_calc_str = ''
    for i in targets_list_calc:
        targets_list_calc_str += (' ' + i)
    print(targets_list_calc_str)


def toxicity_estimation(driver):
    df = pd.read_excel('END_TABLE.xlsx')
    list_of_smiles = df['SMILES'].tolist()
    total_list_of_targets = []
    predicted_LD50 = []
    predicted_toxicity_class = []
    average_similarity = []
    prediction_accuracy = []

    driver.get('https://tox.charite.de/protox3/')
    driver.find_element(By.XPATH, '(//div[@id="ddtopmenubar"]//a[@target="_self"])[2]').click()
    time.sleep(1)
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
            predicted_toxicity_class.append(
                driver.find_element(By.XPATH, '//h1[@style="background:#C8FE2E"]').text[26::])
            time.sleep(1)
        except:
            predicted_toxicity_class.append(0)
        try:
            average_similarity.append(
                driver.find_element(By.XPATH, '(//h1[@style="background:#9ff781"])[1]').text[20::])
            time.sleep(1)
        except:
            average_similarity.append(0)
        try:
            prediction_accuracy.append(
                driver.find_element(By.XPATH, '(//h1[@style="background:#9ff781"])[2]').text[21::])
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
    df_table = pd.DataFrame(np.column_stack((SMILES, name, pathway, superclass, class_col, predicted_LD50,
                                             predicted_toxicity_class, average_similarity, prediction_accuracy)),
                            columns=['SMILES', 'name', 'pathway', 'superclass', 'class', 'predicted_LD50',
                                     'predicted_toxicity_class', 'average_similarity', 'prediction_accuracy'])
    df_table.to_excel('END_TABLE_TOXICITY.xlsx')

def total_target_prediction(driver):
    driver.get('https://prediction.charite.de/subpages/target_prediction.php')
    time.sleep(5)
    df = pd.read_excel('END_TABLE.xlsx')
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


def targets_calculation(driver):
    predicted = pd.read_excel('TOTAL_TARGETS_PREDICTED.xlsx')
    list_predicted = predicted['targets'].tolist()
    proved = pd.read_excel('TOTAL_TARGETS_PROVED.xlsx')
    list_proved = proved['targets'].tolist()
    list_total = []
    list_total.extend(list_predicted)
    list_total.extend(list_proved)
    list_total = list(set(list_total))
    l_t = pd.Series(list_total, name='targets')
    l_t.to_excel('TARGETS_FOR_CALCULATION.xlsx')
    os.remove('TOTAL_TARGETS_PREDICTED.xlsx')
    os.remove('TOTAL_TARGETS_PROVED.xlsx')
    df = pd.read_excel('TARGETS_FOR_CALCULATION.xlsx')
    targets_list_calc = df['targets'].tolist()
    targets_list_calc_str = ''
    for i in targets_list_calc:
        targets_list_calc_str += (' ' + i)
    print(targets_list_calc_str)

    driver.get('http://bioinformatics.sdstate.edu/go/')
    time.sleep(5)
    driver.find_element(By.ID, "input_text").send_keys(targets_list_calc_str)
    time.sleep(10)
    driver.find_element(By.ID, "goButton").click()
    time.sleep(2)
    driver.find_element(By.ID, "selectGO-selectized").click()
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

def total_targets_proved(driver):
    driver.get('https://prediction.charite.de/subpages/target_prediction.php')
    time.sleep(5)
    df = pd.read_excel('END_TABLE.xlsx')
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
    a_ser.to_excel('TOTAL_TARGETS_PROVED.xlsx')

