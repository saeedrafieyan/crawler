import requests
from bs4 import BeautifulSoup
import time

# pics = []
for i in range(1000):
    url = 'https://adsl.tci.ir/panel'

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    image_url = soup.select('#loginCaptchaImage')
    img_data = [img['src'] for img in image_url]
    # pics.append(img_data[0])

    with open(f'pics\second batch/{i}.jpg', 'wb') as handle:
        response = requests.get(img_data[0], stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
    # if i % 20 == 0:
    #     time.sleep(60)

# for i in range(len(pics)):
#     with open(f'pics\second batch/{i}.jpg', 'wb') as handle:
#         response = requests.get(pics[i], stream=True)
#
#         if not response.ok:
#             print(response)
#
#         for block in response.iter_content(1024):
#             if not block:
#                 break
#
#             handle.write(block)

