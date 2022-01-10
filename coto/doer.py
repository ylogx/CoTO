import time

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

TIMEOUT_IN_SECS = 10


class Doer(object):
    def __init__(self, driver: WebDriver) -> None:
        self.driver: WebDriver = driver
        super().__init__()

    def ele_id(self, element_id) -> WebElement:
        return self.driver.find_element(By.ID, element_id)

    def ele_css(self, css_selector) -> WebElement:
        return self.driver.find_element(By.CSS_SELECTOR, css_selector)

    def scroll_to(self, element: WebElement):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def at_url(self, url):
        def there_yet():
            return self.driver.current_url.startswith(url.split("?")[0])

        while not there_yet():
            time.sleep(1)
        return there_yet()

    def click_when_enabled(self, element_id):
        continue_button: WebElement = self.driver.find_element(By.ID, element_id)
        self.wait_till_enabled(element_id=continue_button.id)
        logger.debug(f"Clicking {element_id}.")
        continue_button.click()

    def is_enabled(self, element_id):
        def there_yet():
            return self.driver.find_element(By.ID, element_id).is_enabled()

        while not there_yet():
            time.sleep(1)
        return there_yet()

    def wait_till_enabled(self, element_id):
        logger.debug(f"Waiting for the element {element_id} to be enabled on {self.driver.current_url}")
        WebDriverWait(self.driver, timeout=TIMEOUT_IN_SECS).until(lambda d: self.is_enabled(element_id))

    def wait_a_little(self, secs: int):
        logger.debug(f"Waiting for {secs} seconds on {self.driver.current_url}")
        WebDriverWait(self.driver, timeout=TIMEOUT_IN_SECS).until_not(
            lambda _: time.sleep(secs)
        )
        logger.debug(
            f"After wait, on page: {self.driver.title} w/ url: {self.driver.current_url}"
        )

    def wait_till_url(self, url):
        logger.debug(
            f"Waiting for url change from {self.driver.current_url} to expected: {url}"
        )
        WebDriverWait(self.driver, timeout=180).until(lambda d: self.at_url(url))
        logger.debug(
            f"After wait, on page: {self.driver.title} w/ url: {self.driver.current_url}"
        )
