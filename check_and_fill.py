import os
from selenium import webdriver
from datetime import datetime
from time import sleep


URL = 'https://www.drpciv.ro/drpciv-booking/formular/22/theoryExamination'
EXECUTABLE_PATH = r'-'
REFRESH_DELAY_SEC = 10
ALARM_FILE_NAME = "alarm.mp3"
MONTH_LIMIT = 'mai'

FIRST_NAME = '-'
LAST_NAME = '-'
EMAIL = '-'
REG_NUMBER = '-'


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path=EXECUTABLE_PATH)
    driver.get(URL)
    sleep(1)

    free_day_found = False
    while not free_day_found:
        sleep(REFRESH_DELAY_SEC)
        calendar_wrap = driver.find_element_by_class_name('calendar-wrap')
        calendar_selected_month = calendar_wrap.find_element_by_tag_name('h3')
        calendar_nav_header = calendar_wrap.find_element_by_class_name('calendar-navigation')
        calendar_prev_btn = calendar_nav_header.find_element_by_class_name('prev')
        calendar_next_btn = calendar_nav_header.find_element_by_class_name('next')

        calendar_content = calendar_wrap.find_element_by_class_name('calendar-table').find_element_by_tag_name('tbody')

        for tr in calendar_content.find_elements_by_tag_name('tr'):
            for td in tr.find_elements_by_tag_name('td'):
                if td and td.get_attribute('class').find('available-day') != -1:
                    print(f'First available day: {td.find_element_by_tag_name("div").text} {calendar_selected_month.text}')
                    driver.execute_script("arguments[0].click();", td)

                    free_day_found = True
                    os.system(ALARM_FILE_NAME)
                    break

            if free_day_found:
                break

        if not free_day_found:
            if calendar_selected_month.text.lower().find(MONTH_LIMIT) == -1:
                driver.execute_script("arguments[0].click();", calendar_next_btn)
            elif calendar_selected_month.text.lower().find(MONTH_LIMIT) != -1:
                print(f'Refresh timestamp: {datetime.now().time()}')
                driver.refresh()

    if free_day_found:
        driver.find_element_by_id('last-name').send_keys(LAST_NAME)
        driver.find_element_by_id('first-name').send_keys(FIRST_NAME)
        driver.find_element_by_id('file-number').send_keys(REG_NUMBER)
        driver.find_element_by_id('email').send_keys(EMAIL)
