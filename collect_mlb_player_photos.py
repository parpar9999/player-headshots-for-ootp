import requests
import unidecode
import urllib.request
import os
from bs4 import BeautifulSoup
from PIL import Image

IS_EXIST = True
headshot_path = './mlb_photos/'
headshot_by_team_path = './mlb_photos_by_team/'

team_list = ['orioles', 'redsox', 'whitesox', 'indians', 'tigers', 'astros', 'royals',\
            'angels', 'twins', 'yankees', 'athletics', 'mariners', 'rays', 'rangers',\
            'bluejays', 'nationals', 'cardinals', 'giants', 'padres', 'pirates', 'phillies',\
            'mets', 'brewers', 'marlins', 'dodgers', 'rockies', 'reds', 'cubs', 'braves',\
            'dbacks']

default_url = 'https://www.mlb.com/team/roster/'

fp =  open('same_name.txt', 'w+')

if not IS_EXIST:
    for team_name in team_list:
       path = headshot_by_team_path + team_name + '/'
       os.mkdir(path)

cnt = 2
for team_name in team_list:
    print(team_name)
    url = default_url.replace('team', team_name)
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    players = soup.find_all(class_='info')
    for player in players:
        player = player.find('a')
        p_url = 'https://www.mlb.com' + player['href']
        p_html = requests.get(p_url)
        player = BeautifulSoup(p_html.content, "html.parser").find(class_='player-header__container')
        try:
            player = player.find(class_='player-headshot')
        except Exception as e:
            continue
        name = ''
        try:
            name = player['alt']
        except Exception as e:
            continue
        name = unidecode.unidecode(name).lower().strip()
        name = name.replace('sr.', 'sr')
        name = name.replace('jr.', 'jr')
        print(name)
        file_path = headshot_by_team_path + team_name + '/' + name.replace(' ', '_') + '.png'
        headshot_url = player['src'].strip()
        print(headshot_url)
        headshot = requests.get(headshot_url)
        headshot = headshot.content

        with open(file_path, 'wb') as f:
            f.write(headshot)

        try:
            im = Image.open(file_path)
        except OSError:
            os.remove(file_path)

        file_path = headshot_path + '/' + name.replace(' ', '_') + '.png'
        if os.path.isfile(file_path):
            print(file_path, file=fp)
            file_path = headshot_path + '/' + name.replace(' ', '_') + '_' + team_name.lower() + '.png'

        with open(file_path, 'wb') as f:
            f.write(headshot)

        try:
            im = Image.open(file_path)
        except OSError:
            os.remove(file_path)

        # print(name, ': ', headshot)
    # print('\n'*10)
