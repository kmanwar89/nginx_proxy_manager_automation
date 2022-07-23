# Purpose: Automation the clicking through in Nginx Proxy Manager (NPM) 
# to add proxy hosts
# Programmer: Kadar Anwar
# Language: Python 3.8.9
# Filename: npm_automation.py
# Date: 22 JUL 2022

# Version 1.0 - Initial script, tested & working
    # TODO: accept a list of domains & ports in CSV format to pass through

#from argparse import Action
#from asyncio.constants import SENDFILE_FALLBACK_READBUFFER_SIZE
#rom distutils.spawn import find_executable
import time
import getpass

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By # Specifically needed for identifying elements 'by' a specific attribute
from selenium.webdriver.common.keys import Keys # Used to send keystrokes

# from selenium.webdriver.common.action_chains import ActionChains - Used for sending multiple keys

def main():

    # Gather base facts
    npm_domain = input("Enter Domain Name: ") 
    npm_user = input("Enter login username: ")
    npm_pass = getpass.getpass("Enter Password: ")
    npm_port = input("Enter Port #: ")
    server_IP = "192.168.1.236"
    
    # Setup for selenium magic
    options = Options()
    options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options = options)
    driver.get('https://npm.kadaranwar.com/login')

    # Handling Login
    driver.find_element(By.NAME, "identity").send_keys(npm_user)
    driver.find_element(By.NAME, "secret").send_keys(npm_pass)
    driver.find_element(By.XPATH, "//*[@id=\"login\"]/div/div/div/div/form/div/div/div/div[2]/div[4]/button").click()
    
    # Click through to add a new Proxy host
    driver.find_element(By.XPATH, "//*[@id=\"dashboard\"]/div[2]/div[1]/div/div/div/h4/a/small").click()
    driver.find_element(By.XPATH, "//*[@id=\"nginx-proxy\"]/div/div[2]/div/a[2]").click()

    # Domain name
    driver.find_element(By.XPATH, "//*[@id=\"input-domains-selectized\"]").click()
    driver.find_element(By.XPATH, "//*[@id=\"input-domains-selectized\"]").send_keys(npm_domain)
    driver.find_element(By.XPATH, "//*[@id=\"input-domains-selectized\"]").send_keys(Keys.ENTER)

    # IP address
    driver.find_element(By.XPATH, "//*[@id=\"details\"]/div/div[3]/div/input").click()
    driver.find_element(By.XPATH, "//*[@id=\"details\"]/div/div[3]/div/input").send_keys(server_IP)
    driver.find_element(By.XPATH, "//*[@id=\"details\"]/div/div[3]/div/input").send_keys(Keys.ENTER)

    # Port #
    driver.find_element(By.XPATH, "//*[@id=\"details\"]/div/div[4]/div/input").click()
    driver.find_element(By.XPATH, "//*[@id=\"details\"]/div/div[4]/div/input").send_keys(npm_port)

    # Cache Assets
    driver.find_element(By.XPATH, "//*[@id=\"details\"]/div/div[5]/div/label/span[1]").click()

    # Block exploits
    driver.find_element(By.XPATH, "//*[@id=\"details\"]/div/div[6]/div/label/span[1]").click()

    # Click over to SSL tab
    driver.find_element(By.XPATH, "//*[@id=\"modal-dialog\"]/div/div/div[2]/form/ul/li[3]/a").click()

    # SSL options dropdown
    driver.find_element(By.XPATH, "//*[@id=\"ssl-options\"]/div/div[1]/div/div/div[1]").click()
    driver.find_element(By.XPATH, "//*[@id=\"ssl-options\"]/div/div[1]/div/div/div[2]/div/div[2]").click()

    # Force SSL
    driver.find_element(By.XPATH, "//*[@id=\"ssl-options\"]/div/div[2]/div/label/span[1]").click()

    # HTTP/2 Support
    driver.find_element(By.XPATH, "//*[@id=\"ssl-options\"]/div/div[3]/div/label/span[1]").click()

    # HSTS
    driver.find_element(By.XPATH, "//*[@id=\"ssl-options\"]/div/div[4]/div/label/span[1]").click()

    # HSTS subdomains
    driver.find_element(By.XPATH, "//*[@id=\"ssl-options\"]/div/div[5]/div/label").click()

    # T&C
    driver.find_element(By.XPATH, "//*[@id=\"ssl-options\"]/div/div[9]/div/label/span[1]").click()

    # Submit
    driver.find_element(By.XPATH, "//*[@id=\"modal-dialog\"]/div/div/div[3]/button[2]").click()

    # Short sleep timer while SSL cert is created
    time.sleep(10)

    # Close out the browser once done
    driver.close()

main()