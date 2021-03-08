from bs4 import BeautifulSoup
import requests
import random
import json
import logging
import json


logging.basicConfig(
    level=logging.INFO, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s: %(message)s'
)
logger = logging.getLogger('hoyolab')


REF = [
    'https://mail.yandex.ru/#inbox',
    'https://vk.com/away.php',
    'https://yandex.ru/search/',
    'https://www.google.com/search'
]

UA = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
    ]

def set_sessions():
    request = requests.session()
    headers = {
        "User-Agent": random.choice(UA),
        'Referer': random.choice(REF)
        }
    request.headers.update(headers)

    return request


def parse_hoyoID(browser):
    logger.info('Получаем последний ID')
    actual_id_html = browser.get('https://www.toshima.space/authorize.php?last_id=true&pass=0&id=0&nickname=0&pass=fqlfLFGKQ512')

    soup = BeautifulSoup(actual_id_html.text, 'html.parser')
    actual_id = soup.find('div', class_='actual_id').getText()

    logger.info(f'Последний ID: {actual_id}')
    str_id_offset = int(actual_id)

    logger.info('Начинаем парсинг')
    str_id_offset+=1

    while True:
        logger.info(f'Проверяем ID: {str_id_offset}')
        user = browser.get(f'https://bbs-api-os.hoyolab.com/community/user/wapi/getUserFullInfo?gids=2&uid={str_id_offset}').text
        user_json = json.loads(user)
        try:
            nickname = user_json['data']['user_info']['nickname'];
            notify = user_json['data']['user_info']['community_info']['notify_disable']['follow']

            if len(nickname) > 2:
                logger.info(f'Валидный ID: {str_id_offset} / Никнейм: {nickname} / Выкл. оповещения: {notify}')
                browser.get('http://www.toshima.space/authorize.php?pass=fqlfLFGKQ512&id='+str(str_id_offset)+'&nickname='+nickname)

        except Exception:
            logger.info(f'Пользователь с ID: {str_id_offset} не найден')
        except CertificateError as e:
            log.error(
                'Certificate did not match expected hostname: %s. '
                'Certificate: %s', asserted_hostname, cert
            )

        str_id_offset+=1


if __name__=='__main__':
    session = set_sessions()
    parse_hoyoID(session)
