from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
from bs4 import BeautifulSoup

import pytest


today = datetime.today().date()
format_date = today.strftime("%d/%m/%Y")


def send_notification(time_interval, price):
    print(f"Самое дешевое электричество в промежутке {time_interval} по цене {price} €/kWh")
@pytest.fixture
def page():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://tarifasgasluz.com/comparador/precio-kwh")
    yield driver
    driver.quit()


def extract_price_intervals(driver):
    options = Options()
    options.add_argument("--headless")
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    time_intervals = soup.find_all(class_="template-tlh__colors--hours-info")
    price_intervals = {}
    for time_interval in time_intervals:
        time_text = time_interval.find("span").text.strip()
        price_text = time_interval.find_next(class_="template-tlh__colors--hours-price").text.strip()
        price = float(price_text.split()[0].replace(",", "."))
        price_intervals[time_text] = price

    return price_intervals


def test_search_price_light(page):
    options = Options()
    options.add_argument("--headless")
    driver = page
    price_intervals = extract_price_intervals(page)
    cheap_threshold_price = 0.07
    expensive_threshold_price = 0.12
    cheap_interval_found = False
    expensive_interval_found = False
    cheap_intervals = []
    expensive_intervals = []
    for time_interval, price in price_intervals.items():
        print(f"Time Interval: {time_interval}, Price: {price} €/kWh")
        if price < cheap_threshold_price:
            cheap_interval_found = True
            cheap_intervals.append(time_interval)
        if price > expensive_threshold_price:
            expensive_interval_found = True
            expensive_intervals.append(time_interval)
    if cheap_interval_found:
        print("Уведомление: Дешевая цена электроэнергии в интервалах:", ", ".join(cheap_intervals))
    if expensive_interval_found:
        print("Уведомление: Дорогая цена электроэнергии в интервалах:", ", ".join(expensive_intervals))



