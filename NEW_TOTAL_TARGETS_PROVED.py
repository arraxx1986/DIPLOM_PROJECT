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
driver = f.web_driver()
f.total_targets_proved(driver)
