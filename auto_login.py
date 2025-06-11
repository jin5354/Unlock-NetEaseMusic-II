# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0049F8FF318C89AD737A5923D5C234F905CE860EB424A4AC2DD906E171341BFB9F5050058A6FEA0CEDEB996CDAB917236F7624B4E01ADAE385F402C72A712202D0348ADFC1BFCE972996B954520776C6A98017FE54DFB253A20B2BFCD1F390B535C2652D3A597979319E83F260BF271F2CAEBF2FD6189174385FFEE03372E97995A7AE255EBBD429B446EAE50BB397BF28A5B9B0162A9F1F9FDB0E53EA7127DCD7E2F51B62A6CFE5EC64AE827C8221F2889F2EE978189117C83333424F2706CE4A673BFC275E9DBF567AF2264609E678707625CF3432C353077C8D8E971EBC5D86861E2E2E8419BB4025C699B6E626941138B59DE6FD2D90511D455CD09D335DD496DF5F32E2D0E6E3E8E0707BA0262EBA6740E746BFC7D4FF714B00B5E4114FC89D6D01D858C790C8FFC809A6795BFE8F1B510C92C70FDA2F2A2CDC194D1212D98A641D8AB280324EC7AFB726A7D7DE6F"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
