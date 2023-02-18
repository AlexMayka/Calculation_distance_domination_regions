# Импорт библиотек
# Importing libraries
import time
import pandas as pd
import json
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def connect_web(url_adress):
    """

    :param url_adress:
    :return:
    """
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url_adress)
    time.sleep(5)
    return driver


def search_input(driver, delay, adress):
    try:
        elem_search_string = WebDriverWait(driver, delay) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//input[@class='input__control _bold']")))
        elem_search_string.send_keys(adress)
        elem_search_string.send_keys(Keys.ENTER)
    except Exception:
        print(f'{adress} - не отработал')


def get_coordinates(driver, delay):
    coord = None
    try:
        elem_search_2 = WebDriverWait(driver, delay) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='toponym-card-title-view__coords-badge']")))
        coord = elem_search_2.text
    except:
        try:
            elem_first_list = WebDriverWait(driver, delay) \
                .until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='search-snippet-view__body _type_toponym']")))
            elem_first_list.click()
            get_coordinates(driver, delay)
        except:
            print('Увы и ах')

    try:
        elem_clear = WebDriverWait(driver, 2) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//a[@class='small-search-form-view__pin']")))
    except:
        elem_clear = WebDriverWait(driver, 2) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='small-search-form-view__icon _type_close']")))

    elem_clear.click()
    return coord


def work_selenium(np_search_adress, url_adress):
    driver = connect_web(url_adress)
    delay = 10
    proba = 0
    adress_coord = {}

    for adress in tqdm(np_search_adress):
        time.sleep(1)
        search_input(driver, delay, adress)
        coord = get_coordinates(driver, delay)
        adress_coord[adress] = coord
        with open('..\\data\\adress_coord.json', 'w', encoding='utf-8-sig') as json_f:
           json.dump(adress_coord, json_f)



if __name__ == '__main__':
    url_adress = 'https://yandex.ru/maps'
    df_start_address = pd.read_json('..\\data\\ready_addresses.json')
    new_df = work_selenium(df_start_address['formating_adress'], url_adress)

#305000, Курская область, г Курск, ул Гагарина, д. 22, кор. б, кв. 10