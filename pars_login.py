from bs4 import BeautifulSoup as bs
import requests


URL = 'https://onebill.parsonline.com/'
LOGIN_ROUTE = 'login/'

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/109.0.0.0 Safari/537.36', 'origin': URL, 'referer': URL + LOGIN_ROUTE}

s = requests.session()
login_payload = {
    'Username': 2144250505,
    'Password': 112233,
    'Captcha': 0000
}

login_req = s.post(URL + LOGIN_ROUTE, headers=HEADERS, data=login_payload)
print(login_req.status_code)