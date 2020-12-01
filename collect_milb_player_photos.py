import requests
import unidecode
import urllib.request
import os
import re
import numpy as np
from bs4 import BeautifulSoup
from PIL import Image

IS_EXIST = True
headshot_path = './milb_photos/'
headshot_by_team_path = './milb_photos_by_team/'

team_list = ['aberdeen', 'akron', 'albuquerque', 'altoona', 'amarillo', 'arkansas', 'asheville',\
            'auburn', 'augusta', 'batavia', 'beloit', 'billings', 'biloxi', 'binghamton',\
            'bluefield', 'boise', 'bowie', 'bowling-green', 'bradenton', 'bristol', 'brooklyn',\
            'buffalo', 'burlington-bees', 'burlington-royals', 'carolina-mudcats', 'cedar-rapids', 'charleston', 'charlotte-knights',\
            'charlotte-stone-crabs', 'chattanooga', 'clearwater', 'clinton', 'columbia', 'columbus',\
            'corpus-christi', 'danville', 'dayton', 'daytona', 'delmarva', 'down-east', 'durham',\
            'dunedin', 'el-paso', 'elizabethton', 'erie', 'eugene', 'everett', 'fayetteville',\
            'florida', 'fort-myers', 'fort-wayne', 'frederick', 'fredericksburg', 'fresno',\
            'frisco', 'grand-junction', 'great-falls', 'great-lakes', 'greenville', 'gwinnett',\
            'greensboro', 'hagerstown', 'harrisburg', 'hartford', 'hickory', 'hillsboro', 'hudson-valley',\
            'idaho-falls', 'indianapolis', 'inland-empire', 'iowa', 'jackson', 'jacksonville',\
            'jersey-shore', 'johnson-city', 'jupiter', 'kane-county', 'kannapolis', 'kingsport',\
            'lake-county', 'lake-elsinore', 'lakeland', 'lancaster', 'lansing', 'las-vegas',\
            'lexington', 'louisville', 'lowell', 'lynchburg', 'mahoning-valley', 'memphis', 'midland',\
            'mississippi', 'missoula', 'modesto', 'montgomery', 'myrtle-beach', 'nashville',\
            'new-hampshire', 'norfolk', 'northwest-arkansas', 'norwich', 'ogden', 'oklahoma-city',\
            'omaha', 'orem', 'palm-beach', 'pensacola', 'peoria', 'portland', 'princeton', 'pulaski',\
            'quad-cities', 'rancho-cucamonga', 'reading', 'reno', 'richmond', 'rochester', 'rocket-city',\
            'rocky-mountain', 'rome', 'round-rock', 'sacramento', 'salem', 'salem-keizer', 'salt-lake',\
            'san-antonio', 'san-jose', 'scranton-wb', 'south-bend', 'spokane', 'springfield', 'st-lucie',\
            'state-college', 'staten-island', 'stockton', 'syracuse', 'tacoma', 'tampa', 'tennessee',\
            'toledo', 'trenton', 'tri-city-dust-devils', 'tri-city-valleycats', 'tulsa', 'vancouver',\
            'vermont', 'visalia', 'west-michigan', 'west-virginia-black-bears', 'west-virginia-power',\
            'wichita', 'williamsport', 'wilmington', 'winston-salem', 'wisconsin', 'worcester']

default_url = 'https://www.milb.com/team/roster'

fp =  open('same_name.txt', 'w+')

cnt = 2

if not IS_EXIST:
    for team_name in team_list:
       path = headshot_path + team_name + '/'
       os.mkdir(path)

for team_name in team_list:
    print(team_name)
    url = default_url.replace('team', team_name)
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    players = soup.find_all(class_='player-thumb__back')
    for player in players:
        player = player.find('img')
        name = player['alt']
        name = unidecode.unidecode(name).lower().strip()
        name = name.replace('sr.', 'sr')
        name = name.replace('jr.', 'jr')

        headshot_url = player['src'].strip()
        headshot_url = re.sub('/t[0-9]+/', '/generic/', headshot_url)

        if '.png' in headshot_url:
            file_path = headshot_by_team_path + team_name + '/' + name.replace(' ', '_') + '.png'
        elif '.jpg' in headshot_url:
            file_path = headshot_by_team_path + team_name + '/' + name.replace(' ', '_') + '.jpg'
        else:
            print('new format!!!')
            exit(1)

        headshot = requests.get(headshot_url, verify=False)
        headshot = headshot.content

        with open(file_path, 'wb') as f:
            f.write(headshot)

        try:
            im = Image.open(file_path)
        except OSError:
            os.remove(file_path)

        if '.png' in headshot_url:
            file_path = headshot_path + '/' + name.replace(' ', '_') + '.png'
        elif '.jpg' in headshot_url:
            file_path = headshot_path + '/' + name.replace(' ', '_') + '.jpg'

        if os.path.isfile(file_path):
            print(file_path, file=fp)
            file_path = headshot_path + '/' + name.replace(' ', '_') + '_' + str(cnt) + '.png'
            cnt += 1

        with open(file_path, 'wb') as f:
            f.write(headshot)

        try:
            im = Image.open(file_path)
        except OSError:
            os.remove(file_path)

        print(name, ': ', headshot_url)


    # exit(1)
    # print('\n'*10)
