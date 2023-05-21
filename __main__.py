import json, tracker_urls_scraper
from tracker_data_scraper import TrackerDataScraper



if __name__ == '__main__':
    trackers = tracker_urls_scraper.get_trackers('2023-05-20', '2023-05-21')
    scraper = TrackerDataScraper()
    for t in trackers:
        print(t)
        data = scraper.parse_data(t)
        with open(f"./parsed/{data.get('serverInfo', {}).get('matchId')}.json", 'w') as f:
            json.dump(data, f)
