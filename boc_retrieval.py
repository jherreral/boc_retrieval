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

# To run this in console
# exec(open('boc_retrieval.py').read())


def download_excel_from_current_page():
    # Wait for page to load
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//bch-button[@text='Descargar']"))
    )

    # Click download button
    try:
        download_button = driver.find_element(
            By.XPATH, "//bch-button[@text='Descargar']"
        )
        download_button.click()
    except NoSuchElementException:
        print("No download button found")

    # Wait for page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//button[@role='menuitem']")))

    # Click "Descargar Excel" and save file
    dl_buttons = driver.find_elements(By.XPATH, "//button[@role='menuitem']")
    if dl_buttons:
        driver.execute_script("arguments[0].click()", dl_buttons[0])
    else:
        print("No Excel download button found")


def get_account_balance():
    # Go to account page
    # try:
    #     cta_button = driver.find_element(By.XPATH, "//a[@id='nivel4-41111']")
    #     driver.execute_script("arguments[0].click()", cta_button)
    # except NoSuchElementException:
    #     print("No cuenta corriente button found")
    #     return
    driver.get(
        "https://portalpersonas.bancochile.cl/mibancochile-web/front/persona/index.html#/movimientos/cuenta/saldos-movimientos/"
    )
    download_excel_from_current_page()


def get_credit_card_balance():
    # Jump to Tarjeta Credito page
    # try:
    #     tcred_button = driver.find_element(By.XPATH, "//a[@id='nivel4-41311']")
    #     driver.execute_script("arguments[0].click()", tcred_button)
    # except NoSuchElementException:
    #     print("No tarjeta de credito button found")
    #     return

    driver.get(
        "https://portalpersonas.bancochile.cl/mibancochile-web/front/persona/index.html#/tarjeta-credito/consultar/saldos"
    )
    # Wait for page to load
    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Seleccionar otra tarjeta')]")
        )
    )
    try:
        card_field = driver.find_element(By.XPATH, "//*[contains(text(),'Signature')]")
        card_field.click()
    except NoSuchElementException:
        print("No Signature card found, attempting to change card.")

        select_card_button = driver.find_element(
            By.XPATH,
            "//*[contains(text(),'Seleccionar otra tarjeta')]",
        )
        print(select_card_button)
        select_card_button.click()

        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'Signature')]")
            )
        )
        radio_button = driver.find_element(
            By.XPATH, "//*[contains(text(),'Signature')]"
        )
        radio_button.click()
        accept_button = driver.find_element(By.XPATH, "//*[contains(text(),'Aceptar')]")
        accept_button.click()

    download_excel_from_current_page()


# Set options
firefox_options = FirefoxOptions()
firefox_options.set_preference("browser.download.folderList", 2)
firefox_options.set_preference("browser.download.dir", "D:\\Repos\\boc_retrieval\\")

# Install geckodriver
driver = webdriver.Firefox(
    service=FirefoxService(GeckoDriverManager().install()), options=firefox_options
)

# Get credentials
with open("credentials.json", "r") as infile:
    credentials = json.load(infile)
login_page = credentials["login_page"]
my_username = credentials["username"]
my_password = credentials["password"]

# Launch browser and navigate to website
driver.get(login_page)

# Enter credentials
username_field = driver.find_element(By.ID, "iduserName")
password_field = driver.find_element(By.NAME, "userpassword")
username_field.send_keys(my_username)
password_field.send_keys(my_password)
password_field.send_keys(Keys.RETURN)

# Wait for page to load
wait = WebDriverWait(driver, 10)
wait.until(
    EC.presence_of_element_located((By.ID, "btn-home_CuentaCorrienteMonedaLocal"))
)
# driver.implicitly_wait(8)

get_account_balance()

# Go to Home
driver.get(
    "https://portalpersonas.bancochile.cl/mibancochile-web/front/persona/index.html#/home"
)
# Wait for page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='nivel4-41311']")))

get_credit_card_balance()
