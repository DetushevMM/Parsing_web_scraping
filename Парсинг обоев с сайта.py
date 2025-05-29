# Парсинг всего сайта и скачивание файлов внутри него
import os
import requests
import fake_useragent
from bs4 import BeautifulSoup

# Создаем папку, если она ещё не существует
os.makedirs('image', exist_ok=True)

# В нашем случае страницы перебираются по номерам в ссылке. 
# Создадим переменную для перебора страниц по номерам
storage_number = 1
# для азвания изображения
image_number = 0

link = f'https://zastavok.net'

# Создадим цикл для перебора страниц
for storage in range(2):
    # Подделка User-Agent для обхода блокировок
    headers = {
    'User-Agent': fake_useragent.UserAgent().random
    }

    response = requests.get(f"{link}/{storage_number}", headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

    # Инспектирум сайт и ищем блок div, где размещены все фото в виде класса
    block = soup.find('div', class_ = "block-photo")

    # При инспектировании сайта в блоке div class_ = block-photo ищем сласс каждого фото
    all_image = block.find_all('div', class_ = "short_full")

    # print(all_image)

    # При помощи break получим первое значение блока, 
    # чтобы понять, какие данные можно парсить из текущего тэга
    for image in all_image:
        # print(image)
        # break  # нашли наш тэг = а (<a href="/animals/65135-akula_more_vid_sverhu_pesok.html")
        image_link = image.find('a').get('href')
        download_storage = requests.get(f'{link}{image_link}', headers=headers).text
        # print(image_link)
        download_soup = BeautifulSoup(download_storage, 'lxml')
        
        dowload_block = download_soup.find('div', class_ = "image_data").find('div', class_ = "block_down")
        result_link = dowload_block.find('a').get('href')
        # print(result_link)  # мы получили код картинки (текст на скачивание картинки)
        
        image_bytes = requests.get(f'{link}{result_link}', headers=headers).content  # с помощью content можно скачать любой файл в интернете

        # скачивание картинок
        with open(f'image/{image_number}.jpg', 'wb') as file:
            file.write(image_bytes)
        image_number += 1
        print(f'Изображение {image_number}.jpg успешно скачено')
