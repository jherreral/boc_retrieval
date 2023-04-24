from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
import requests
from bs4 import BeautifulSoup
import json

#To run this in console
# exec(open('boc_retrieval.py').read())

#Set options
firefox_options = FirefoxOptions()
firefox_options.set_preference("browser.download.folderList",2)
firefox_options.set_preference("browser.download.dir","D:\\Repos\\boc_retrieval\\")

# Install geckodriver
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=firefox_options)

# Get credentials
with open("credentials.json", "r") as infile:
    credentials = json.load(infile)
login_page = credentials["login_page"]
my_username = credentials["username"]
my_password = credentials["password"]

# Launch browser and navigate to website
driver.get(login_page)

# Enter credentials
username_field = driver.find_element(By.ID ,"iduserName")
password_field = driver.find_element(By.NAME,"userpassword")
username_field.send_keys(my_username)
password_field.send_keys(my_password)
password_field.send_keys(Keys.RETURN)

# Wait for page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, "btn-home_CuentaCorrienteMonedaLocal")))
# driver.implicitly_wait(8)

# Go to account page
try:
    modal_close_button = driver.find_element(By.XPATH,"//button[@class='btn default btn pull-right']")
    modal_close_button.click()
except NoSuchElementException:
    print("No modal found")

# Go to account page
try:
    account_button = driver.find_element(By.ID,"btn-home_CuentaCorrienteMonedaLocal")
    driver.execute_script("arguments[0].click()",account_button)
except NoSuchElementException:
    print("No account button found")

# Wait for page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, "//bch-button[@text='Descargar']")))

# Click download button
try:
    download_button = driver.find_element(By.XPATH,"//bch-button[@text='Descargar']") 
    download_button.click()
except NoSuchElementException:
    print("No download button found")

# Wait for page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, "//button[@role='menuitem']")))

# Click "Descargar Excel" and save file
dl_buttons = driver.find_elements(By.XPATH,"//button[@role='menuitem']")
if dl_buttons:
    driver.execute_script("arguments[0].click()",dl_buttons[0])
else:
    print("No Excel download button found")

