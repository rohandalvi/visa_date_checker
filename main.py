#!/usr/bin/env python

import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from mail import Mail


def check_dates():
    ais_portal_username = os.getenv('ais_portal_username')
    ais_portal_password = os.getenv('ais_portal_password')
    # chrome_web_driver_exec_path = os.getenv('chrome_web_driver_exec_path')
    locations_to_check = ['Vancouver', 'Ottawa', 'Calgary']
    user_email = os.getenv('user_email')
    email_subject = 'Visa date available'
    ais_url = "https://ais.usvisa-info.com/en-ca/niv/users/sign_in"

    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    # driver = webdriver.Chrome(executable_path=chrome_web_driver_exec_path)
    actions = ActionChains(driver)

    driver.get(ais_url)
    input_element = driver.find_element(by=By.ID, value="user_email")
    input_element.send_keys(ais_portal_username)
    input_element = driver.find_element(by=By.ID, value="user_password")
    input_element.send_keys(ais_portal_password)
    checkbox = driver.find_element(by=By.CLASS_NAME, value="icheckbox")
    if not checkbox.is_selected():
        checkbox.click()
    element = driver.find_element(by=By.CSS_SELECTOR, value="input[name=commit]")
    element.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Continue")))

    # click on continue
    element = driver.find_element(by=By.LINK_TEXT, value="Continue")
    element.click()

    # Wait for next page for calendar to show
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Schedule Appointment")))

    # click on Schedule appointment accordion
    element = driver.find_element(by=By.LINK_TEXT, value="Schedule Appointment")
    element.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[1]/div/div/div[2]/p[2]/a")))

    time.sleep(2)
    # click on Schedule appointment button within the accordion
    element = driver.find_element(by=By.XPATH,
                                  value="/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[1]/div/div/div[2]/p[2]/a")
    element.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.ID, "appointments_consulate_appointment_facility_id")))

    for location in locations_to_check:

        location_select = Select(driver.find_element(by=By.ID, value="appointments_consulate_appointment_facility_id"))
        location_select.select_by_visible_text(location)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.ID, "appointments_consulate_appointment_date_input")))  # this is not working, using sleep for now

        time.sleep(3)
        driver.find_element(by=By.ID, value="appointments_consulate_appointment_date_input").click()
        datepicker = driver.find_element(by=By.XPATH, value="/html/body/div[5]")
        actions.move_to_element(datepicker).click().perform()

        time.sleep(2)
        calendar = driver.find_element(by=By.CLASS_NAME, value="ui-datepicker-group-first")

        current_calendar_body = calendar.find_element(by=By.XPATH,
                                                      value="//table[@class='ui-datepicker-calendar']/tbody")
        try:
            day_box = current_calendar_body.find_element(by=By.XPATH,
                                                         value=".//td[not(contains(@class,'ui-state-disabled'))]")
            day = day_box.find_element(by=By.XPATH, value=".//a").text
            month_picker = calendar.find_element(by=By.CLASS_NAME, value="ui-datepicker-month")
            year_picker = calendar.find_element(by=By.CLASS_NAME, value="ui-datepicker-year")
            year = year_picker.text
            month = month_picker.text
            # I only want to check dates until January, change this if you need to check further dates
            if month == "February":
                driver.find_element(by=By.ID, value="appointments_consulate_address").click()
                return
            body = "{0}/{1}/{2} is available at location {3}".format(month, day, year, location)
            Mail().send(user_email, email_subject, body)
        except NoSuchElementException:
            while True:
                next_month = driver.find_element(by=By.XPATH, value="/html/body/div[5]/div[2]/div/a")
                next_month.click()
                try:
                    calendar = driver.find_element(by=By.CLASS_NAME, value="ui-datepicker-group-first")
                    month_picker = calendar.find_element(by=By.CLASS_NAME, value="ui-datepicker-month")
                    year_picker = calendar.find_element(by=By.CLASS_NAME, value="ui-datepicker-year")
                    month = month_picker.text

                    # I only want to check dates until January, change this if you need to check further dates
                    if month == "February":
                        driver.find_element(by=By.ID, value="appointments_consulate_address").click()
                        break
                    year = year_picker.text
                    current_calendar_body = calendar.find_element(by=By.XPATH,
                                                                  value="//table[@class='ui-datepicker-calendar']/tbody")
                    day_box = current_calendar_body.find_element(by=By.XPATH,
                                                                 value=".//td[not(contains(@class,'ui-state-disabled'))]")
                    day = day_box.find_element(by=By.XPATH, value=".//a").text
                    body = "{0}/{1}/{2} is available at location {3}".format(month, day, year, location)
                    Mail().send(user_email, email_subject, body)
                    print(body)
                    break
                except NoSuchElementException:
                    print("Checking {0} for dates in {1}".format(location, month))
                    continue


if __name__ == '__main__':
    check_dates()
