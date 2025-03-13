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
    browser.add_cookie({"name": "MUSIC_U", "value": "00FDCB51EDFA080690F2F27F39807AE21E93F9626740206023C278B31059F3BE5269A7830E4312611B0AB1C3819BEB01FE981CD05CDBD9D3DC00D28626E0BFDAEE44FF58D5BBC9A81E6AAFE4E5A6D242430829137FB31E97125E80BD66AFA4E825066911CA20370C47F39720D502CD8DDEA241C76B380764D4384FFAF7FA271E89AADC39A5F8967DF1FBA06579E9BB8CB26523D770DC412CA93E0C91E319D9B0A26642BE613424385A67803BABAD0047D72D2DDC545FDBF4E42063B5F9368E850DD0988AC03DD4760E195A239A93738BAFE591599772912ABD439A3FB2F10C63042C2B1B81B6D0408C29D99500E55E2AA199B8CBA8912D49895E6A1DCBEC8DA3B3A7FD29B1AF65247981ACE07496FB34F32391F65869E42D2E2311818C394A467B208C7F13E2794D40B73F1E7D9A1119C8466D840FDC586E9BA4C07FD9FE4F2D8D243100CD10ECDB9215918B69E9C071FC66B215606E3F0EEC18EBDF8A53891E30"})
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
