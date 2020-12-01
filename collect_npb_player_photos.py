import requests
import unidecode
import urllib.request
import os
from bs4 import BeautifulSoup
from PIL import Image

headshot_path = './npb_photos/'

source_url = 'https://npb.jp/bis/eng/players/active/team'

team_list = ['rst_g.html', 'rst_l.html', 'rst_db.html', 'rst_h.html', 'rst_t.html',\
            'rst_e.html', 'rst_c.html', 'rst_m.html', 'rst_d.html', 'rst_f.html', 'rst_s.html', 'rst_b.html']

cnt = 2
i = 1

for team in team_list:
    url = source_url.replace('team', team)
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    players = soup.find_all(class_='player_unit_1')

    for player in players:
        src_url =  'https://npb.jp' + player['href']
        try:
            html2 = requests.get(src_url)
        except:
            continue

        soup2 = BeautifulSoup(html2.content, "html.parser")
        player = soup2.find(id="pc_v_photo")
        player = player.find('img')
        try:
            headshot_url = player['src'].strip()
        except TypeError:
            continue

        name = player['title'].split(',')
        name = unidecode.unidecode(name[1]).lower().strip() + '_' + unidecode.unidecode(name[0]).lower().strip()
        name = name.replace('sr.', 'sr')
        name = name.replace('jr.', 'jr')
        name = name.replace(' ', '_')

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
