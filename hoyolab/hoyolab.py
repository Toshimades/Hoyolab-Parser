from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

import random
import re
import warnings
import json
import string
from pyfiglet import Figlet

warnings.filterwarnings('ignore')


REF = [
    'https://mail.yandex.ru/#inbox',
    'https://vk.com/away.php',
    'https://yandex.ru/search/',
    'https://www.google.com/search'
]
UAS = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
    ]

FOLLOWERS_SPAM = True
LIKES_SPAM = True
COMMENTS_SPAM = False

def setup():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")

    browser = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_options)
    browser.implicitly_wait(10) # seconds

    W = (random.randint(1024,1920))
    H = (random.randint(768,1080))
    browser.set_window_size(W, H)
    browser.implicitly_wait(10)

    return browser



def set_sessions(browser):
    request = requests.session()
    headers = {
        "User-Agent": random.choice(UAS),
        'Referer': random.choice(REF)
        }
    request.headers.update(headers)
    cookies = browser.get_cookies()
    for cookie in cookies:
        request.cookies.set(cookie['name'], cookie['value'])

    return request







def parse_hoyoID(browser):
    print('Получаем последний ID')
    browser.get('https://www.toshima.space/authorize.php?last_id=true&pass=0&id=0&nickname=0&pass=fqlfLFGKQ512')
    str_id_offset = int(browser.find_element_by_class_name("actual_id").text);
    print('Последний ID: ' + str(str_id_offset))
    print('Начинаем парсинг')
    str_id_offset+=1
    infinity = 1
    while infinity < 10:
        print('Проверяем ID: '+ str(str_id_offset))
        browser.get('https://www.hoyolab.com/genshin/accountCenter/gameRecord?id='+ str(str_id_offset))
        nickname = browser.find_element_by_class_name("mhy-account-center-user__name").text;
        if len(nickname) > 2:
            print('Валидный ID: '+ str(str_id_offset) +' Никнейм: '+nickname)
            browser.get('http://toshima.space/authorize.php?pass=fqlfLFGKQ512&id='+str(str_id_offset)+'&nickname='+nickname)
        str_id_offset+=1





if __name__=='__main__':
    rend = Figlet(font='slant')
    print (rend.renderText('HoYoLab'))
    browser = setup()
    set_sessions(browser)
    parse_hoyoID(browser)
