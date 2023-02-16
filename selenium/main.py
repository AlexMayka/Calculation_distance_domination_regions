# Импорт библиотек
# Importing libraries

import logging
import time
import pandas as pd
import numpy as np
import json
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def work_selenium(url_ad, new_df):
    driver = webdriver.Chrome()
    driver.get(r'https://yandex.ru/maps')
    time.sleep(5)
    delay = 10
    proba = 0
    for i in tqdm(url_ad['clear']):
        # try:
        print(i)
        elem_search_string = WebDriverWait(driver, delay) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='search-form-view__input']")))
        elem_search_string.click()
        elem_search_string = WebDriverWait(driver, delay) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//input[@class='input__control _bold']")))
        elem_search_string.send_keys(i)

        elem_search_string = WebDriverWait(driver, delay) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//input[@class='input__control _bold']")))
        elem_search_string.send_keys(Keys.RETURN)
        try:
            elem_search_2 = WebDriverWait(driver, delay) \
                .until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='toponym-card-title-view__coords-badge']")))
            new_df[i] = elem_search_2.text
            print(elem_search_2.text)
            time.sleep(3)
            proba += 1
        except:
            new_df[i] = 'не найдено'
            print("Увы")
            time.sleep(3)
            proba += 1

        with open('adresa1.json', 'w', encoding='utf-8-sig') as json_f:
            json.dump(new_df, json_f)


        if proba % 200 == 0:
            driver.close()
            time.sleep(60)
            driver = webdriver.Chrome()
            driver.get(r'https://yandex.ru/maps/193/voronezh/?ll=39.200292%2C51.660779&z=12')
            time.sleep(5)

        # except Exception as ex:
        #     print(ex)
    return new_df
    # time.sleep(1000)
    # except Exception as Error_connect_selenium:
    #     print(f'Error connecting to site. {Error_connect_selenium}')
    #     return False

def work_selenium1(url_ad, new_df):
    # try:
    driver = webdriver.Chrome()
    #print(url_ad[url_ad.columns[2]][0])
    driver.get(r'https://snipp.ru/tools/address-coord')
    time.sleep(5)
    delay = 20
    proba = 0
    for i in tqdm(url_ad['clear'].iloc[1467:]):
        # try:
        elem_search_string = WebDriverWait(driver, delay) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//ymaps[@class='ymaps-b-form-input__hint-wrap ymaps-b-form-input__hint-wrap_visibility_visible']")))
        elem_search_string.click()
        elem_search_string = WebDriverWait(driver, delay) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//input[@class='ymaps-b-form-input__input']")))
        elem_search_string.send_keys(i)
        elem_button = WebDriverWait(driver, delay) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//ymaps[@class='ymaps-b-form-button__text']")))
        elem_button.click()
        # elem_search_string = WebDriverWait(driver, delay) \
        #     .until(EC.presence_of_element_located(
        #     (By.XPATH, "//ymaps[@class='ymaps-b-form-button__content']")))
        # elem_search_string.send_keys(Keys.RETURN)
        time.sleep(1)
        try:
            # searchTextBox = driver.find_element_by_xpath("//input[@class='snp-form-input font-pre']")
            elem_search_2 = WebDriverWait(driver, delay) \
                .until(EC.presence_of_element_located(
                (By.XPATH, "//input[@class='snp-form-input font-pre']")))
            new_df[i] = elem_search_2.get_property('value')
            proba += 1
            driver.refresh()
        except:
            new_df[i] = 'не найдено'
            proba += 1
            driver.refresh()

        with open('adresa1.json', 'w', encoding='utf-8-sig') as json_f:
            json.dump(new_df, json_f)


        # if proba % 200 == 0:
        #     driver.close()
        #     time.sleep(60)
        #     driver = webdriver.Chrome()
        #     driver.get(r'https://yandex.ru/maps/193/voronezh/?ll=39.200292%2C51.660779&z=12')
        #     time.sleep(5)

        # except Exception as ex:
        #     print(ex)
    return new_df
    # time.sleep(1000)
    # except Exception as Error_connect_selenium:
    #     print(f'Error connecting to site. {Error_connect_selenium}')
    #     return False

if __name__ == '__main__':
    new_df = {}
    df = pd.read_csv('adress.csv')
    print(df)
    new_df = work_selenium(df, new_df)



    # with open('sksksks.json', 'r', encoding='utf-8-sig') as json_f:
    #     print(json.load(json_f))
    # # df_verified_inn = work_selenium(logger, inn_list)
    # # df_verified_inn.to_csv(f'Result_work_selenium.csv', index=False, encoding='utf-8-sig')

