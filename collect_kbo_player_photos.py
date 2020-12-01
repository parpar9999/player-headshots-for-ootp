import requests
import unidecode
import urllib.request
import os
from bs4 import BeautifulSoup
from PIL import Image

headshot_path = './kbo_photos/'

source_url = 'https://mykbostats.com/teams/TEAM/roster'

team_list = ['1-Doosan-Bears', '4-Hanwha-Eagles', '5-Kia-Tigers', '23-Kiwoom-Heroes',\
            '22-KT-Wiz', '6-LG-Twins', '2-Lotte-Giants', '9-NC-Dinos', '9-NC-Dinos', '3-Samsung-Lions',\
            '3-Samsung-Lions', '7-SK-Wyverns']

cnt = 2
i = 1

for team in team_list:
    url = source_url.replace('TEAM', team)
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    players = soup.find_all(class_="player-link")

    for player in players[1:][::2]:
        name = player.text
        if '-' in name:
            name = name.split(' ')
            name = name[1].strip() + ' ' + name[0].strip()
        name = unidecode.unidecode(name).lower().strip()
        name = name.replace('sr.', 'sr')
        name = name.replace('jr.', 'jr')
        name = name.replace(' ', '_')
        src_url =  'https://mykbostats.com' + player['href']
        try:
            html2 = requests.get(src_url)
        except:
            continue

        soup2 = BeautifulSoup(html2.content, "html.parser")
        player = soup2.find(class_="player-photo")
        try:
            headshot_url = 'https://mykbostats.com/' + player['src'].strip()
        except TypeError:
            continue

        print(name, ': ', headshot_url)

        headshot = requests.get(headshot_url)
        headshot = headshot.content

        file_path = headshot_path + '/' + name + '.png'

        with open(file_path, 'wb') as f:
            f.write(headshot)

        try:
            im = Image.open(file_path)
        except OSError:
            os.remove(file_path)
        i += 1


            # print(name, ': ', headshot)
        # print('\n'*10)
