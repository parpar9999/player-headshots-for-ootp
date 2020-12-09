import requests
import unidecode
import urllib.request
import os
from bs4 import BeautifulSoup
from PIL import Image

IS_EXIST = True
headshot_path = './foreign_photos/'

source_url = 'https://www.baseball-reference.com/register'
l_url = 'https://www.baseball-reference.com'

fp =  open('error.log', 'w')

cnt = 2
i = 1

url = source_url
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")

temp = None
leagues = soup.find_all(class_='formfield')
for league in leagues:
    if 'League' in str(league):
        tmp = league
        break
leagues = BeautifulSoup(str(tmp), "html.parser")
leagues = leagues.find_all('option')[1:]
for league in leagues:
    league_url = l_url + league['value']
    print('-'*5, league.text, '-'*5)
    try:
        html2 = requests.get(league_url)
    except:
        print(name, ': ', src_url, file=fp)
        continue
    soup2 = BeautifulSoup(html2.content, "html.parser")
    teams = soup2.find(id="all_standings_pitching")
    teams = BeautifulSoup(str(teams).replace('<!--', '').replace('-->', ''), "html.parser").find_all('a')

    for team in teams:
        print('-'*5, team.text, '-'*5)
        team_url = 'https://www.baseball-reference.com' + team['href']
        try:
            html2 = requests.get(team_url)
        except:
            print(name, ': ', src_url, file=fp)
            continue
        soup2 = BeautifulSoup(html2.content, "html.parser")
        players = soup2.find(id='all_standard_roster')
        a = str(players).split('<tbody>')[1].split('</tbody>')[:-1]
        players = BeautifulSoup(a[0], "html.parser")
        players = players.find_all('a')

        for player in players:
            # player = player.find('a')
            name = player.text
            name = unidecode.unidecode(name).lower().strip()
            name = name.replace('sr.', 'sr')
            name = name.replace('jr.', 'jr')

            src_url = 'https://www.baseball-reference.com' + player['href']

            try:
                html2 = requests.get(src_url)
            except:
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
                    print(name, ': ', 'not found')
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


                # print(name, ': ', headshot)
            # print('\n'*10)
