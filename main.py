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

directory = os.getcwd() #проверяем наличие основного файла с SMILES
files = os.listdir(directory)
if 'END_TABLE.xlsx' not in files:
    print("Для работы программы необходим файл xlsx сданными SMILES вторичных метаболитов и их классификацией")
    answer_1 = input('Создать файл с классификацией и данными SMILES? (да/нет)     ')
    if answer_1 == 'да':
        plant_name = input('Введите латинское название растения:  ')
        print('ожидайте..........')
        flag = 0
        try:
            driver = f.web_driver()
            f.sdf_download(plant_name, driver)
        except:
            flag = 1
        if flag == 0:
            list_of_smiles = f.smiles_to_xlsx()
        else:
            print('Для данного растения в базе данных отсутствуют известные вещества')
        f.create_END_TABLE(list_of_smiles)
        print('в директории с программой создана таблица с данными SMILES')
    else:
        print('Завершение работы программы.')
else:
    print('Файл с данными SMILES уже присуствует в директории. Выберите дльнейшие действия.')
    print('1 - прогноз токсичности')
    print('2 - прогноз белковых мишений и влияние на организм')

answer_2 = input('Ведите 1 или 2:    ')
if answer_2 == '1':
    driver = f.web_driver()
    f.toxicity_estimation(driver)
elif answer_2 == '2':
    driver = f.web_driver()
    f.total_target_prediction(driver)
    f.total_targets_proved(driver)
    f.targets_calculation(driver)
else:
    print('Введено неверное число. Завершение работы программы.')
