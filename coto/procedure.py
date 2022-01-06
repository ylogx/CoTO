from selenium.webdriver.remote.webdriver import WebDriver


def new_slot(driver: WebDriver):
    driver.get("http://selenium.dev")

    driver.quit()
