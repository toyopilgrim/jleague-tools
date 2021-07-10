# -*- coding: utf-8 -*-

import datetime
import json
from json import JSONEncoder

import requests
from bs4 import BeautifulSoup

clubs = [
    {
        "id": "nagasaki",
        "category": "j2",
        "name": "長崎"
    },
    {
        "id": "kawasakif",
        "category": "j1",
        "name": "川崎Ｆ"
    },
]


class ClubOutput:
    def __init__(self, club_id, category, match_days):
        self.id = club_id
        self.category = category
        self.matchDays = match_days


class MatchDay:
    def __init__(self, location, date, time, opponent, is_home):
        self.location = location
        self.date = date.isoformat()
        self.time = time
        self.opponent = opponent
        self.is_home = is_home


class TypeEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def get_content():
    base_url = "https://www.jleague.jp/match/search/" + c.get("category") + "/all/" + c.get("id")
    page = requests.get(base_url).content
    soup = BeautifulSoup(page, "html.parser")
    return soup.findAll("section", {"class": "matchlistWrap"})


def extract_jp_date(block):
    date_string = block.find('h4', {"class", "leftRedTit"}).get_text()
    split_string = date_string.split("(", 1)
    sub_string = split_string[0]
    return sub_string


def get_stadium(block):
    s = block.find('td', {'class': 'stadium'}).get_text(',').split(',')
    time = s[0]
    if time == "未定":
        time = "TBD"
    location = s[1]
    return [time, location]


def get_opponent_name(own_name, left, right):
    if own_name == left:
        return right
    if own_name == right:
        return left


for c in clubs:
    match_days = []
    for b in get_content():
        date = datetime.datetime.strptime(extract_jp_date(b), '%Y年%m月%d日').date()

        stadium = get_stadium(b)

        game_table = b.find('table', {"class": "gameTable"})
        left = game_table.find('td', {'class': 'clubName leftside'}).find('a').get_text()
        right = game_table.find('td', {'class': 'clubName rightside'}).find('a').get_text()
        opponent = get_opponent_name(c.get("name"), left, right)
        is_home = opponent == right

        match_days.append(MatchDay(stadium[1], date, stadium[0], opponent, is_home))

    output = ClubOutput(c.get("id"), c.get("category"), match_days)
    print(json.dumps(output.__dict__, ensure_ascii=False, indent=4, cls=TypeEncoder))