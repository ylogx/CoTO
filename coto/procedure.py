from loguru import logger
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver

from coto.data import HealthInfo
from coto.doer import Doer


def new_slot(driver: WebDriver, info: HealthInfo):
    doer: Doer = Doer(driver)
    accept_terms(driver, doer)
    doer.wait_a_little(secs=2)
    fill_hc_info(driver, doer, info)
    rest(driver, doer, info)


def rest(driver: WebDriver, doer: Doer, info: HealthInfo):
    # Wait until, url is 'https://covid19.ontariohealth.ca/app-identity?viewId=U5GBUDFZ526Z'
    doer.wait_a_little(secs=3)

    # Wait until url is: https://covid19.ontariohealth.ca/app-menu?viewId=SME7NFFT945B
    # Click #booking_button

    # Wait until url is: https://covid19.ontariohealth.ca/booking-home?viewId=SME7NFFT945B
    # Click radio #fld_booking-home_eligibility_group_noGroup_label
    no_group_radio = doer.ele_id("fld_booking-home_eligibility_group_noGroup_label")
    doer.scroll_to(no_group_radio)
    no_group_radio.click()

    # Wait until enabled #schedule_button
    # Click #schedule_button

    # Wait until https://vaccine.covaxonbooking.ca/location-search?config=4b7b8b6d-8848-454f-a61b-1926f4d5011e
    doer.ele_id("location-search-address").send_keys(info.postal_code)

    i_agree_btn = doer.ele_css("button.tw-w-full")
    # Wait until enabled: i_agree_btn
    i_agree_btn.click()

    # First Location Option: div.tw-border:nth-child(1)
    # Loc Title: div.tw-border:nth-child(1) > div:nth-child(1) > h2:nth-child(1)
    loc_name = doer.ele_css(
        "div.tw-border:nth-child(1) > div:nth-child(1) > h2:nth-child(1)"
    ).text
    logger.info(f"First location is {loc_name}")

    # Click button: div.tw-border:nth-child(1) > div:nth-child(2) > button:nth-child(1)
    availability_btn = doer.ele_css(
        "div.tw-border:nth-child(1) > div:nth-child(2) > button:nth-child(1)"
    )
    availability_btn.click()
    # Second loc: div.tw-border:nth-child(2) > div:nth-child(2) > button:nth-child(1)

    # https://vaccine.covaxonbooking.ca/personal-details?config=4b7b8b6d-8848-454f-a61b-1926f4d5011e
    # #q-patient-email
    doer.ele_id("q-patient-email").send_keys(info.email)
    doer.ele_id("q-patient-mobile").send_keys(info.phone)
    # Click something

    # https://vaccine.covaxonbooking.ca/additional-information?config=4b7b8b6d-8848-454f-a61b-1926f4d5011e
    # Click No: label.tw-flex:nth-child(2)
    doer.ele_css("label.tw-flex:nth-child(2)").click()
    # button.tw-w-full:nth-child(1)
    doer.ele_css("button.tw-w-full:nth-child(1)").click()

    # https://vaccine.covaxonbooking.ca/confirmation?config=4b7b8b6d-8848-454f-a61b-1926f4d5011e
    status_info = doer.ele_css("h1.tw-text-n800").text
    # div.tw-p-6
    booking_info = doer.ele_css("div.tw-p-6").text
    driver.save_screenshot("current-booking.png")

    # driver.quit()


def accept_terms(driver: WebDriver, doer: Doer):
    driver.get("https://covid19.ontariohealth.ca/")

    doer.wait_a_little(secs=2)

    # terms_checkbox = doer.ele_id("acceptedTerm1")
    terms_checkbox = doer.ele_css("#terms-label .fas.fa-square.fa-stack-2x")
    logger.debug(
        f"Terms Checkbox: {terms_checkbox.id} {terms_checkbox.text} {terms_checkbox.tag_name} {terms_checkbox.location} {terms_checkbox.__dict__}"
    )
    doer.scroll_to(terms_checkbox)

    ActionChains(driver).move_to_element(terms_checkbox).click(terms_checkbox).perform()
    doer.wait_a_little(secs=1)

    doer.click_when_enabled(element_id="continue_button")


def fill_hc_info(driver: WebDriver, doer: Doer, info: HealthInfo):
    doer.wait_till_url(
        "https://covid19.ontariohealth.ca/app-identity?viewId=U5GBUDFZ526Z"
    )

    logger.info("Filling hc info.")
    doer.ele_id("hcn").send_keys(info.hc_num)
    doer.ele_id("vcode").send_keys(info.hc_suffix)
    doer.ele_id("scn").send_keys(info.hc_back)
    doer.ele_id("dob").send_keys(info.dob)
    doer.ele_id("postal").send_keys(info.postal_code)

    # Wait until continue_button
    doer.click_when_enabled(element_id="continue_button")
