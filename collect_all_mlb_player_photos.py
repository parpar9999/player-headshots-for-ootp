import requests
import unidecode
import urllib.request
import os
from bs4 import BeautifulSoup
from PIL import Image

IS_EXIST = True
headshot_path = './mlb_photos_all/'

source_url = 'https://www.mlb.com/players'

fp =  open('error.log', 'w')

cnt = 2
i = 1

html = requests.get(source_url)
soup = BeautifulSoup(html.content, "html.parser")

players = soup.find_all(class_='p-related-links__link')
for player in players:
    name = player.text
    name = unidecode.unidecode(name).lower().strip()
    name = name.replace('sr.', 'sr')
    name = name.replace('jr.', 'jr')

    src_url = 'https://www.mlb.com' + player['href']
    # print(src_url)
    try:
        html2 = requests.get(src_url)
    except:
        print(name, ': ', src_url, file=fp)
        continue

    soup2 = BeautifulSoup(html2.content, "html.parser")
    player = soup2.find(class_="player-headshot")
    try:
        headshot_url = player['src'].strip()
    except TypeError:
        print(name, ': ', src_url, file=fp)
        continue

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
