from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from bs4 import BeautifulSoup
from utils import map_name_parser
import chromedriver_autoinstaller, time, pytz, requests


def parse_kills(kills_table):
    kills = []
    soup = BeautifulSoup(kills_table, 'html.parser')
    for tr in soup.find_all('tr'):
        kills.append({
            'time': tr.find_all('td')[0].string,
            'distance': tr.find_all('td')[1].string,
            'killer': tr.find_all('td')[2].string,
            'killerTeam': tr.find_all('td')[2]['class'][0].replace('color_', ''),
            'weapon': tr.find_all('td')[3].string.replace('[', '').replace(']', ''),
            'victim': tr.find_all('td')[4].string,
            'victimTeam': tr.find_all('td')[4]['class'][0].replace('color_', ''),
        })
    return kills


def parse_chat(chat_table):
    chat = []
    soup = BeautifulSoup(chat_table, 'html.parser')
    for tr in soup.find_all('tr'):
        chat.append({
            'time': tr.find_all('td')[0].string,
            'chatType': tr.find_all('td')[1].string,
            'player': tr.find_all('td')[2].string,
            'message': tr.find_all('td')[3].string
        })
    return chat


def parse_revives(revives_table):
    revives = []
    soup = BeautifulSoup(revives_table, 'html.parser')
    for tr in soup.find_all('tr'):
        revives.append({
            'time': tr.find_all('td')[0].string,
            'medic': tr.find_all('td')[1].string,
            'revived': tr.find_all('td')[2].string,
            'team': tr.find_all('td')[1]['class'][0].replace('color_', '')
        })
    return revives


def parse_vehicles_destroyed(vehicles_destroyed_table):
    vehicles_destroyed = []
    soup = BeautifulSoup(vehicles_destroyed_table, 'html.parser')
    for tr in soup.find_all('tr'):
        vehicles_destroyed.append({
            'time': tr.find_all('td')[0].string,
            'destroyer': tr.find_all('td')[1].string,
            'destroyerTeam': tr.find_all('td')[1]['class'][0].replace('color_', ''),
            'vehicle': tr.find_all('td')[2].string,
            'vehicleTeam': tr.find_all('td')[2]['class'][0].replace('color_', '')
        })
    return vehicles_destroyed


def parse_serverinfo(match_id, serverinfo_table):
    serverinfo = {}
    soup = BeautifulSoup(serverinfo_table, 'html.parser')
    serverinfo.update({
        'matchId': match_id,
        soup.find_all('tr')[0].find_all('td')[0].string.lower().replace(' ', '_'): soup.find_all('tr')[0].find_all('td')[1].string,
        soup.find_all('tr')[1].find_all('td')[0].string.lower().replace(' ', '_'): soup.find_all('tr')[1].find_all('td')[1].string,
        soup.find_all('tr')[2].find_all('td')[0].string.lower().replace(' ', '_'): soup.find_all('tr')[2].find_all('td')[1].string,
        soup.find_all('tr')[3].find_all('td')[0].string.lower().replace(' ', '_'): soup.find_all('tr')[3].find_all('td')[1].string,
        soup.find_all('tr')[4].find_all('td')[0].string.lower().replace(' ', '_'): soup.find_all('tr')[4].find_all('td')[1].string,
        soup.find_all('tr')[5].find_all('td')[0].string.lower().replace(' ', '_'): soup.find_all('tr')[5].find_all('td')[1].string,
        soup.find_all('tr')[6].find_all('td')[0].string.lower().replace(' ', '_'): soup.find_all('tr')[6].find_all('td')[1].string,
        })
    return serverinfo


def parse_kit_allocations(parse_kit_allocations_table):
    parse_kit_allocations = []
    soup = BeautifulSoup(parse_kit_allocations_table, 'html.parser')
    for tr in soup.find_all('tr'):
        parse_kit_allocations.append({
            'time': tr.find_all('td')[0].string,
            'player': tr.find_all('td')[1].string,
            'playerTeam': tr.find_all('td')[1]['class'][0].replace('color_', ''),
            'kit': tr.find_all('td')[2].string,
        })
    return parse_kit_allocations


def get_map_info(serverinfo):
    url = 'https://www.realitymod.com/mapgallery/json/{map_name}/{mode}.json'
    map_name = serverinfo.get('map_name', '').lower().replace('_', '').replace(' ', '')
    map_name = map_name_parser.MAPS.get(map_name, map_name)
    mode = serverinfo.get('map_mode', '').lower() + '_' + serverinfo.get('map_layer', '').lower()
    print(url.format(map_name=map_name, mode=mode))
    resp = requests.get(url.format(map_name=map_name, mode=mode))
    if resp.status_code == 200:
        return resp.json().get('Team')
    else:
        print(f'Error getting map info: {str(resp.status_code)}')


def install_chromedriver():
    chromedriver_autoinstaller.install()


class TrackerDataScraper:
    def __init__(self):
        install_chromedriver()
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("headless")
        self.driver = webdriver.Chrome(chrome_options=self.options)

    def open_tracker(self, tracker_url):
        match_id = tracker_url.split('/')[-1].replace('tracker_', '').replace('.PRdemo', '')
        self.driver.get(tracker_url)
        time.sleep(30)

        kills_table = self.driver.find_element(By.XPATH, "//table[@id='killsTable']").get_attribute("outerHTML")
        chat_table = self.driver.find_element(By.XPATH, "//table[@id='chatTable']").get_attribute("outerHTML")
        revives_table = self.driver.find_element(By.XPATH, "//table[@id='revivesTable']").get_attribute("outerHTML")
        vehicles_destroyed_table = self.driver.find_element(By.XPATH, "//table[@id='vehicleDestroyersTable']").get_attribute(
            "outerHTML")
        kit_allocations_table = self.driver.find_element(By.XPATH, "//table[@id='kitAllocationsTable']").get_attribute("outerHTML")
        serverinfo_table = self.driver.find_element(By.XPATH, "//table[@id='serverinfoTable']").get_attribute("outerHTML")

        return match_id, kills_table, chat_table, revives_table, vehicles_destroyed_table, kit_allocations_table, \
            serverinfo_table

    def parse_data(self, tracker_url):
        match_id, kills_table, chat_table, revives_table, vehicles_destroyed_table, kit_allocations_table, \
            serverinfo_table = self.open_tracker(tracker_url)
        kills = parse_kills(kills_table)
        chat = parse_chat(chat_table)
        revives = parse_revives(revives_table)
        vehicles_destroyed = parse_vehicles_destroyed(vehicles_destroyed_table)
        kit_allocations = parse_kit_allocations(kit_allocations_table)
        serverinfo = parse_serverinfo(match_id, serverinfo_table)

        match_start_date = datetime.strptime(serverinfo['round_start_time'], '%a, %d %b %Y %H:%M:%S %Z')
        match_start_date = match_start_date.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('America/Sao_Paulo')).isoformat()
        serverinfo.update({'round_start_time': match_start_date})

        map_info = get_map_info(serverinfo)
        consolidated = {
            'serverInfo': serverinfo,
            'mapInfo': {'Team1': map_info[0], 'Team2': map_info[1]} if map_info else {},
            'kills': kills,
            'chat': chat,
            'revives': revives,
            'kit_allocations': kit_allocations,
            'vehicles_destroyed': vehicles_destroyed,
        }

        return consolidated
