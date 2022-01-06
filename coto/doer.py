import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


TIMEOUT_IN_SECS = 10


class Doer(object):
    def __init__(self, driver: WebDriver) -> None:
        self.driver: WebDriver = driver
        super().__init__()

    def ele_id(self, id) -> WebElement:
        return self.driver.find_element(By.ID, id)

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

    def wait_till_enabled(self, element_id):
        logger.debug(
            f"Waiting for the element {element_id} to be enabled on {driver.current_url}"
        )
        WebDriverWait(self.driver, timeout=TIMEOUT_IN_SECS).until(
            lambda d: d.find_element(By.ID, element_id).is_enabled()
        )

    def wait_a_little(self, secs: int):
        logger.debug(f"Waiting for {secs} seconds on {driver.current_url}")
        WebDriverWait(self.driver, timeout=TIMEOUT_IN_SECS).until_not(
            lambda _: time.sleep(secs)
        )
        logger.debug(
            f"After wait, on page: {driver.title} w/ url: {driver.current_url}"
        )

    def wait_till_url(self, url):
        logger.debug(
            f"Waiting for url change from {driver.current_url} to expected: {url}"
        )
        WebDriverWait(self.driver, timeout=180).until(lambda d: at_url(d, url))
        logger.debug(
            f"After wait, on page: {driver.title} w/ url: {driver.current_url}"
        )
