import requests
import unidecode
import urllib.request
import os
from bs4 import BeautifulSoup
from PIL import Image
from bs4 import Comment

IS_EXIST = True
headshot_path = './milb_photos_reference/'

source_url = 'https://www.baseball-reference.com/register/affiliate.cgi'

fp =  open('error.log', 'w')

cnt = 2
i = 1

url = source_url
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")

teams = soup.find_all('ul')[5].find_all('a')

for team in teams:
    print('-'*5, team.text, '-'*5)
    team_url = 'https://www.baseball-reference.com' + team['href']
    try:
        html2 = requests.get(team_url)
    except:
        print(name, ': ', src_url, file=fp)
        continue

    soup2 = BeautifulSoup(html2.content, "html.parser")
    ts = soup2.find_all('tr')[1]

    ts = ts.find_all('td')
    for t in ts:
        print('-'*5, t.text, '-'*5)
        t = t.find('a')
        try:
            url = 'https://www.baseball-reference.com' + t['href']
        except:
            continue
        try:
            html2 = requests.get(url)
        except:
            continue
        soup2 = BeautifulSoup(html2.content, "html.parser")

        soup2 = str(soup2).replace('<!--', '').replace('-->', '')
        soup2 = BeautifulSoup(soup2, 'html.parser')
        players = soup2.find_all(class_='table_container')

        tmp = []
        for p in players[:2]:
            p = p.find_all('a')
            tmp += p
        players = tmp

        for player in players:
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
                try:
                    headshot_url = player.find('img')['src'].strip()
                except:
                    continue

            print(name, ': ', headshot_url)

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
