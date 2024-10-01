import time
import os
import pandas as pd
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import xlsxwriter
import functions as f


print("Данная программа позволяет провести прогноз воздействия вторичных метаболитор растительного объекта на организм")
print("На первом этапе сформируем файл xlsx со SMILES вторичных метаболитов и их классификацией")


driver = f.web_driver()
plant_name = input('Введите латинское название растения:  ')
flag = 0
try:
    f.sdf_download(plant_name, driver)
except:
    flag = 1
if flag == 0:
    list_of_smiles = f.smiles_to_xlsx()
else:
    print('Для данного растения в базе данных отсутствуют известные вещества')
f.create_END_TABLE(list_of_smiles)