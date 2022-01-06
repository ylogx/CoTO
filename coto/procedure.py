import time

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


def new_slot(driver: WebDriver):
    driver.get("https://shubham.chaudhary.xyz/blog/")

    logger.debug(f"Driver properties: {driver.__dict__}")
    logger.info(f"Opened page titled: {driver.title}")

    WebDriverWait(driver, timeout=10).until_not(lambda _: time.sleep(5))

    driver.quit()
