import requests
import unidecode
import urllib.request
import os
from bs4 import BeautifulSoup
from PIL import Image

headshot_path = './cpbl_photos/'

source_url = 'http://cpblstats.com/team'

team_list = ['chinatrust-brothers', 'fubon-guardians', 'rakuten-monkeys', 'uni-lions',\
            'wei-chuan-dragons']

cnt = 2
i = 1

for team in team_list:
    url = source_url.replace('team', team)
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    players = soup.find_all("tr")

    for player in players[1:]:
        player = player.find_all("td")

        name = player[2].text
        if '-' in name:
            name = name.split(' ')
            name = name[1].strip() + ' ' + name[0].strip()
        name = unidecode.unidecode(name).lower().strip()
        name = name.replace('sr.', 'sr')
        name = name.replace('jr.', 'jr')
        name = name.replace(' ', '_')
        try:
            src_url = player[1]['data-sheets-hyperlink'].replace('&amp;', '&')
        except:
            continue
        try:
            html2 = requests.get(src_url)
        except:
            continue

        soup2 = BeautifulSoup(html2.content, "html.parser")
        player = soup2.find(class_="player_info_pic")
        try:
            headshot_url = player.find('img')['src']
        except:
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
