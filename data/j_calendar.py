# -*- coding: utf-8 -*-

import datetime
import requests
from bs4 import BeautifulSoup

clubs = [
    {
        "id": "nagasaki",
        "category": "j2",
        "name": "長崎"
    },
]


def get_content():
    base_url = "https://www.jleague.jp/match/search/" + c.get("category") + "/all/" + c.get("id")
    print(base_url)
    page = requests.get(base_url).content
    soup = BeautifulSoup(page, "html.parser")
    return soup.findAll("section", {"class": "matchlistWrap"})


def extract_jp_date(block):
    date_string = block.find('h4', {"class", "leftRedTit"}).get_text()
    split_string = date_string.split("(", 1)
    sub_string = split_string[0]
    return sub_string


def get_title(block):
    game_table = block.find('table', {"class": "gameTable"})
    left = game_table.find('td', {'class': 'clubName leftside'}).find('a').get_text()
    right = game_table.find('td', {'class': 'clubName rightside'}).find('a').get_text()
    return left + " vs " + right


def get_stadium(block):
    s = block.find('td', {'class': 'stadium'}).get_text(',').split(',')
    time = s[0]
    if time == "未定":
        time = "TBD"
    location = s[1]
    return [time, location]


for c in clubs:
    for b in get_content():
        date = datetime.datetime.strptime(extract_jp_date(b), '%Y年%m月%d日').date()

        stadium = get_stadium(b)
        title = get_title(b)

        print(date)
        print(stadium[1])
        print(stadium[0])
        print(title)
        print("-------------------")
