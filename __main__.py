import json
from tracker_data_scraper import TrackerDataScraper


if __name__ == '__main__':
    scraper = TrackerDataScraper()
    tracker_url = 'http://prserver.servegame.com:666/Server/PRServer/BattleRecorder/tracker_viewer/index.html?demo=../Server01/tracker/tracker_2023_05_14_20_09_07_saaremaa_gpm_cq_64.PRdemo'
    data = scraper.parse_data(tracker_url)
    with open(f"./parsed/{data.get('serverInfo', {}).get('matchId')}.json") as f:
        json.dump(data, f)
