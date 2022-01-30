from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from xml.etree.ElementTree import iselement

email = input("Enter email to continue: ")
password = input("Enter password for " + email + ":")

url = "https://www.youtube.com/feed/channels"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(url)

#Inputs "email" Variable
WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]')))
driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(email + Keys.ENTER)

#Inputs "password" Variable
WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password + Keys.ENTER)

#Detects if 2-Step Verification is Present
if driver.current_url.__contains__("https://accounts.google.com/signin/v2/challenge/") or driver.find_element(By.XPATH, '//*[@id="headingText"]/span').text == "2-Step Verification":
    print("                                                                   ")
    print("2-Step Verification DETECTED! Complete verification to continue..." )
    print("                                                                   ")
else:
    pass

#Selects "[1]" (1st) YouTube Account
WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="contents"]/ytd-account-item-renderer[1]/tp-yt-paper-icon-item')))
driver.find_element(By.XPATH, '//*[@id="contents"]/ytd-account-item-renderer[1]/tp-yt-paper-icon-item').click()

#Scrapes Channel Names of all Active Subscriptions
channel_names = driver.find_elements(By.CLASS_NAME, 'style-scope ytd-channel-name')

#Opens & Writes list of Active Subscriptions to "subscriptions.txt"
textfile = open("subscriptions.txt", "a")
for i in channel_names:
    print(i.text)
    print(i.text, file=textfile)
textfile.close()

driver.quit()