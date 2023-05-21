from bs4 import BeautifulSoup
from datetime import datetime
import requests, os

TRACKER_ROOT_URL = 'http://prserver.servegame.com:666/Server/PRServer/BattleRecorder/'


def get_page_html():
    resp = requests.get(TRACKER_ROOT_URL + '?srv=1')
    page = None
    if resp.status_code == 200:
        page = resp.content
    return page


def get_trackers(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    page = get_page_html()
    soup = BeautifulSoup(page, 'html.parser')
    links = []
    for url in soup.findAll('a', href=True, string='Tracker'):
        if ("rubbish" not in url['href'].lower()) and ("incomplete" not in url['href'].lower()):
            tracker_date = datetime.strptime('-'.join(url['href'].split('/')[-1].split('_')[1:4]), '%Y-%m-%d')
            if start_date <= tracker_date <= end_date:
                links.append(TRACKER_ROOT_URL + url['href'])
    return links


def get_tracker_files(path):
    files = os.listdir(path)
    tracker_files = []
    for f in files:
        if f.endswith('.PRdemo'):
            tracker_files.append(path + f)
    return tracker_files