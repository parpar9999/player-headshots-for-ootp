import requests
import unidecode
import urllib.request
import os
from bs4 import BeautifulSoup
from PIL import Image

IS_EXIST = True
headshot_path = './mlb_photos_reference/'

source_url = 'https://www.baseball-reference.com/players/'

fp =  open('error.log', 'w')

a2z = [chr(i) for i in range(97, 97+26)]

cnt = 2
i = 1

for char in a2z:
    url = source_url + char
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    players = soup.find_all('ul')[4]
    players = players.find_all('strong')

    for player in players:
        player = player.find('a')
        name = player.text
        name = unidecode.unidecode(name).lower().strip()
        name = name.replace('sr.', 'sr')
        name = name.replace('jr.', 'jr')

        src_url = 'https://www.baseball-reference.com' + player['href']

        try:
            html2 = requests.get(src_url)
        except:
            print(name, ': ', src_url, file=fp)
            continue

        soup2 = BeautifulSoup(html2.content, "html.parser")
        player = soup2.find(class_="media-item multiple")
        try:
            headshot_url = player.find('img')['src'].strip()
        except:
            player = soup2.find(class_="media-item")
            headshot_url = player.find('img')['src'].strip()

        print(i, ': ', headshot_url)
        headshot = requests.get(headshot_url)
        headshot = headshot.content

        file_path = headshot_path + '/' + name.replace(' ', '_') + '.png'

        with open(file_path, 'wb') as f:
            f.write(headshot)

        try:
            im = Image.open(file_path)
        except OSError:
            os.remove(file_path)
        i += 1


            # print(name, ': ', headshot)
        # print('\n'*10)
