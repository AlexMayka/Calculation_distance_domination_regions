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
    Создаем элемент класса webdriver и переходим на страницу по url-адресу
    :param url_adress: url-адрес сайта
    :return: driver: элемент класса webdriver
    """

    driver = webdriver.Chrome('chromedriver.exe')
    driver.get(url_adress)
    time.sleep(5)
    return driver


def search_input(driver, delay, adress):
    """
    Функция для внесения данных в поисковую форму
    :param driver: элемент класса webdriver
    :param delay: время ожидания
    :param adress: адрес
    """

    try:
        # Поиск формы ввода на сайте
        elem_search_string = WebDriverWait(driver, delay) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//input[@class='input__control _bold']")))
        # Вписываем данные в форму
        elem_search_string.send_keys(adress)
        # Запускаем поиск
        elem_search_string.send_keys(Keys.ENTER)
    except Exception:
        print(f'{adress} - не отработал')


def get_coordinates(driver, delay):
    """
    Функция для получения координат адреса
    :param driver: элемент класса webdriver
    :param delay: время ожидания
    :return: coord: координаты адреса
    """
    coord = None
    try:
        # Поиск координат на сайте
        elem_search_2 = WebDriverWait(driver, delay) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='toponym-card-title-view__coords-badge']")))
        # Запись в переменную координат адреса
        coord = elem_search_2.text
    except:
        try:
            # Если поиск выдал несколько результатов. выбираем 1 в списке элемент
            elem_first_list = WebDriverWait(driver, delay) \
                .until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='search-snippet-view__body _type_toponym']")))
            elem_first_list.click()
            # Запускаем повторно функцию
            get_coordinates(driver, delay)
        except:
            print('Увы и ах')

    # Очищаем форму для записи
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
    """
    Основная функция работы скрипта
    :param np_search_adress: список адресов
    :param url_adress: url-адрес сайта
    """
    driver = connect_web(url_adress)  # Настройка selenium
    delay = 10  # Время ожидания
    adress_coord = {}  # Словарь для записи результатов работы

    for adress in tqdm(np_search_adress):
        time.sleep(1)
        search_input(driver, delay, adress)  # Вносим адрес в поисковую форму
        coord = get_coordinates(driver, delay)  # Получаем координаты адреса
        adress_coord[adress] = coord  # Записываем результат в словарь
        with open('..\\data\\adress_coord.json', 'w', encoding='utf-8-sig') as json_f:
            # Записываем словарь в файл
            json.dump(adress_coord, json_f)


if __name__ == '__main__':
    url_adress = 'https://yandex.ru/maps'  # Сайт "Яндекс карты"
    df_start_address = pd.read_json('..\\data\\ready_addresses.json')  # Полученные адреса (после работы тетрадки)
    work_selenium(df_start_address['formating_adress'][0:499], url_adress)  # Запуск основной функции

# 305000, Курская область, г Курск, ул Гагарина, д. 22, кор. б, кв. 10
