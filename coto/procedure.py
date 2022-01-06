import time

from selenium.webdriver.remote.webdriver import WebDriver


def new_slot(driver: WebDriver):
    driver.get("https://shubham.chaudhary.xyz/blog/")

    time.sleep(5)
    driver.quit()
