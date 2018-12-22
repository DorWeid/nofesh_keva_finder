# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import logging

# Import smtplib for the actual sending function
import smtplib
email = 'YOUR_EMAIL_HERE'
password = 'YOUR_PW_HERE'

# Import the email modules we'll need
from email.mime.text import MIMEText

logging.basicConfig(format='%(asctime)s %(message)s')

LANDING_PAGE_URL = "http://www.idf.il"
ID_NUMBER = "YOUR_ID"
PASSWORD = "YOUR_PW"
HOTELS = ["יערות הכרמל", "בראשית", "גורדוניה", "דן אילת"]
PORT = 8000

def configDriver():
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--window-size=1920x1080")
  chrome_driver = os.getcwd() +"\\chromedriver.exe"
  driver = webdriver.Chrome(chrome_options=chrome_options)
  return driver

driver = configDriver()

def landing():
  driver.get(LANDING_PAGE_URL)
  # Navigate to prat sub domain
  driver.find_element_by_class_name("nav-btn").click()

def login():
  driver.find_element_by_id("IdNumber").send_keys(ID_NUMBER)
  driver.find_element_by_id("Password").send_keys(PASSWORD)
  driver.find_element_by_id("submitLogin").click()

def navToVacationSite():
  # Wait until page has loaded properly
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "הנופש"))).click()

def searchHotels(sleepBetweenSearches, onHotelFound, onHotelNotFound):
  # Iterate on list of hotels
  for hotel in HOTELS:
    driver.find_element_by_id("areaHoteltxt").clear()
    time.sleep(1)
    # NOTE: needed to use decode() here for some reason.. 
    driver.find_element_by_id("areaHoteltxt").send_keys(hotel.decode("utf-8"))
    time.sleep(1)
    # driver.find_element_by_id("searchButton").click()
    driver.execute_script("document.getElementById('searchButton').click()")
    time.sleep(5)

    try:
      driver.find_element_by_class_name("nohResultsSection")
      onHotelNotFound(hotel)

    except NoSuchElementException:
      onHotelFound(hotel)
    finally:
      time.sleep(sleepBetweenSearches)

def hotelFound(hotel):
  logging.warning('Found hotel: %s', hotel)

def hotelNotFound(hotel):
  logging.warning('Not Found hotel: %s', hotel)

def automation():
  landing()
  login()
  navToVacationSite()
  searchHotels(10, hotelFound, hotelNotFound)

# server = smtplib.SMTP('smtp.gmail.com:587')
# server.ehlo()
# server.starttls()
# server.login(email,password)
# msg = 'Found hotel abc'
# server.sendmail(email, email, msg)
# server.quit()

count = 1
while True:
  automation()
  logging.info('Finished Run #%d', count)
  count += 1
  time.sleep(60)
