import time

from loguru import logger
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

import coto.data

TIMEOUT_IN_SECS = 10


def new_slot(driver: WebDriver, info: coto.data.HealthInfo):
    accept_terms(driver)
    wait_a_little(driver, secs=2)
    fill_hc_info(driver, info)
    # Wait until, url is 'https://covid19.ontariohealth.ca/app-identity?viewId=U5GBUDFZ526Z'
    wait_a_little(driver, secs=3)

    # Wait until url is: https://covid19.ontariohealth.ca/app-menu?viewId=SME7NFFT945B
    # Click #booking_button

    # Wait until url is: https://covid19.ontariohealth.ca/booking-home?viewId=SME7NFFT945B
    # Click radio #fld_booking-home_eligibility_group_noGroup_label
    scroll_to(driver, driver.find_element(By.ID, 'fld_booking-home_eligibility_group_noGroup_label'))
    driver.find_element(By.ID, 'fld_booking-home_eligibility_group_noGroup_label').click()

    # Wait until enabled #schedule_button
    # Click #schedule_button

    # Wait until https://vaccine.covaxonbooking.ca/location-search?config=4b7b8b6d-8848-454f-a61b-1926f4d5011e
    driver.find_element(By.ID, 'location-search-address').send_keys(info.postal_code)

    i_agree_btn: WebElement = driver.find_element(By.CSS_SELECTOR, 'button.tw-w-full')
    # Wait until enabled: i_agree_btn
    i_agree_btn.click()

    # First Location Option: div.tw-border:nth-child(1)
    # Loc Title: div.tw-border:nth-child(1) > div:nth-child(1) > h2:nth-child(1)
    loc_name = driver.find_element(By.CSS_SELECTOR, 'div.tw-border:nth-child(1) > div:nth-child(1) > h2:nth-child(1)').text
    logger.info(f"First location is {loc_name}")

    # Click button: div.tw-border:nth-child(1) > div:nth-child(2) > button:nth-child(1)
    availability_btn = driver.find_element(By.CSS_SELECTOR, 'div.tw-border:nth-child(1) > div:nth-child(2) > button:nth-child(1)')
    availability_btn.click()
    # Second loc: div.tw-border:nth-child(2) > div:nth-child(2) > button:nth-child(1)

    # https://vaccine.covaxonbooking.ca/personal-details?config=4b7b8b6d-8848-454f-a61b-1926f4d5011e
    # #q-patient-email
    driver.find_element(By.ID, 'q-patient-email').send_keys(info.email)
    driver.find_element(By.ID, 'q-patient-mobile').send_keys(info.phone)
    # Click something

    # https://vaccine.covaxonbooking.ca/additional-information?config=4b7b8b6d-8848-454f-a61b-1926f4d5011e
    # Click No: label.tw-flex:nth-child(2)
    driver.find_element(By.CSS_SELECTOR, 'label.tw-flex:nth-child(2)').click()
    # button.tw-w-full:nth-child(1)
    driver.find_element(By.CSS_SELECTOR, 'button.tw-w-full:nth-child(1)').click()

    # https://vaccine.covaxonbooking.ca/confirmation?config=4b7b8b6d-8848-454f-a61b-1926f4d5011e
    status_info = driver.find_element(By.CSS_SELECTOR, 'h1.tw-text-n800').text
    # div.tw-p-6
    booking_info = driver.find_element(By.CSS_SELECTOR, 'div.tw-p-6').text
    driver.save_screenshot('current-booking.png')

    # driver.quit()


def accept_terms(driver: WebDriver):
    driver.get("https://covid19.ontariohealth.ca/")

    wait_a_little(driver, secs=2)

    # terms_checkbox: WebElement = driver.find_element(By.ID, "acceptedTerm1")
    terms_checkbox: WebElement = driver.find_element(By.CSS_SELECTOR, "#terms-label .fas.fa-square.fa-stack-2x")
    logger.debug(f"Terms Checkbox: {terms_checkbox.id} {terms_checkbox.text} {terms_checkbox.tag_name} {terms_checkbox.location} {terms_checkbox.__dict__}")
    scroll_to(driver, terms_checkbox)

    ActionChains(driver).move_to_element(terms_checkbox).click(terms_checkbox).perform()
    WebDriverWait(driver, timeout=TIMEOUT_IN_SECS).until_not(lambda _: time.sleep(1))

    click_when_enabled(driver, element_id='continue_button')


def fill_hc_info(driver: WebDriver, info: coto.data.HealthInfo):
    wait_till_url(driver, 'https://covid19.ontariohealth.ca/app-identity?viewId=U5GBUDFZ526Z')

    logger.info('Filling hc info.')
    driver.find_element(By.ID, 'hcn').send_keys(info.hc_num)
    driver.find_element(By.ID, 'vcode').send_keys(info.hc_suffix)
    driver.find_element(By.ID, 'scn').send_keys(info.hc_back)
    driver.find_element(By.ID, 'dob').send_keys(info.dob)
    driver.find_element(By.ID, 'postal').send_keys(info.postal_code)

    # Wait until continue_button
    click_when_enabled(driver, element_id='continue_button')

# Helpers


def scroll_to(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)


def at_url(driver, url):
    def there_yet():
        return driver.current_url.startswith(url.split('?')[0])

    while not there_yet():
        time.sleep(1)
    return there_yet()


def click_when_enabled(driver, element_id):
    continue_button: WebElement = driver.find_element(By.ID, element_id)
    wait_till_enabled(driver, element_id=continue_button.id)
    logger.debug(f'Clicking {element_id}.')
    continue_button.click()


def wait_till_enabled(driver, element_id):
    logger.debug(f"Waiting for the element {element_id} to be enabled on {driver.current_url}")
    WebDriverWait(driver, timeout=TIMEOUT_IN_SECS).until(
        lambda d: d.find_element(By.ID, element_id).is_enabled())


def wait_a_little(driver: WebDriver, secs: int):
    logger.debug(f"Waiting for {secs} seconds on {driver.current_url}")
    WebDriverWait(driver, timeout=TIMEOUT_IN_SECS).until_not(lambda _: time.sleep(secs))
    logger.debug(f"After wait, on page: {driver.title} w/ url: {driver.current_url}")


def wait_till_url(driver, url):
    logger.debug(f"Waiting for url change from {driver.current_url} to expected: {url}")
    WebDriverWait(driver, timeout=180).until(lambda d: at_url(d, url))
    logger.debug(f"After wait, on page: {driver.title} w/ url: {driver.current_url}")
