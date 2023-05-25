import json, tracker_urls_scraper, shutil, os, wget
from tracker_data_scraper import TrackerDataScraper

LOCAL_TRACKERS_PATH = "D:\\Projetos\\ProjectRealityTrackerData\\local_trackers\\"


def move_trackers(tracker_name):
    current_path_abs = '.\\local_trackers\\' + tracker_name
    processed_path = '.\\local_trackers\\processed\\' + tracker_name
    shutil.move(current_path_abs, processed_path)


def save_file(tracker_data):
    with open(f"./parsed/{tracker_data.get('serverInfo', {}).get('matchId')}.json", 'w') as f:
        json.dump(tracker_data, f)


def parse_remote_trackers(start_date, end_date):
    trackers = tracker_urls_scraper.get_trackers(start_date, end_date)
    scraper = TrackerDataScraper()
    for t in trackers:
        print(t)
        data = scraper.parse_data(t)
        save_file(data)


def parse_local_trackers(path):
    trackers = tracker_urls_scraper.get_tracker_files(path)
    scraper = TrackerDataScraper()
    for t in trackers:
        print(t)
        tracker_name = t.split("\\")[-1]
        data = scraper.parse_data(t, is_uploaded=True)
        save_file(data)
        move_trackers(tracker_name)


if __name__ == '__main__':
    parse_remote_trackers('2023-05-24', '2023-05-24')
    parse_local_trackers(LOCAL_TRACKERS_PATH)
