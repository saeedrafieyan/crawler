import requests
from bs4 import BeautifulSoup
import time

pics = []
for i in range(100):
    url = 'https://adsl.tci.ir/panel'

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    image_url = soup.select('#loginCaptchaImage')
    img_data = [img['src'] for img in image_url]
    pics.append(img_data[0])
    time.sleep(5)

for i in range(len(pics)):
    with open(f'pics/{i}.jpg', 'wb') as handle:
        response = requests.get(pics[i], stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
print(img_data)
