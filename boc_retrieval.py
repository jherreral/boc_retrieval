from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
import requests
from bs4 import BeautifulSoup
import json

# Install geckodriver
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

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
# wait = WebDriverWait(driver, 10)
# wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
# driver.implicitly_wait(8)


# Go to account page
# try:
#     modal_close_button = driver.find_element(By.XPATH,"//button[@id='modal_emergente_close']")
#     modal_close_button.click()
# except NoSuchElementException:
#     print("No modal found")

# account_button = driver.find_element(By.ID,"btn-home_CuentaCorrienteMonedaLocal")
# #account_button = driver.find_element(By.LINK_TEXT,"Cuenta Corriente")
# driver.execute_script("arguments[0].scrollIntoView();", account_button)
# account_button.click()

# Click download button
# download_button = driver.find_element_by_xpath("//button[@id='download']")
# download_button.click()

# # Save file
# url = driver.current_url
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')
# filename = soup.find('filename').text
# with open(filename, 'wb') as f:
#     f.write(response.content)
