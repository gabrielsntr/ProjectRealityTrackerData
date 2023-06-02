import json, tracker_urls_scraper, shutil, os, wget
from tracker_data_scraper import TrackerDataScraper

LOCAL_TRACKERS_PATH = "D:\\Projetos\\ProjectRealityTrackerData\\local_trackers\\"


def download_tracker(url):
    if not (os.path.exists(LOCAL_TRACKERS_PATH + url.split('/')[-1])\
            or os.path.exists(LOCAL_TRACKERS_PATH + 'processed\\' + url.split('/')[-1])):
        wget.download(url, LOCAL_TRACKERS_PATH)
        return True
    else:
        print("File already downloaded. Skipping...")
        return False


def move_trackers(tracker_name):
    current_path_abs = '.\\local_trackers\\' + tracker_name
    processed_path = '.\\local_trackers\\processed\\' + tracker_name
    try:
        shutil.move(current_path_abs, processed_path)
    except Exception as e:
        print(f"Error moving files: {str(e)}")


def save_file(tracker_data):
    with open(f"./parsed/{tracker_data.get('serverInfo', {}).get('matchId')}.json", 'w') as f:
        json.dump(tracker_data, f)


def parse_remote_trackers(start_date, end_date):
    trackers = tracker_urls_scraper.get_trackers(start_date, end_date)
    scraper = TrackerDataScraper()
    for t in trackers:
        print(t)
        tracker_name = t.split("/")[-1]
        download_url = t.split('?')
        download_url = download_url[0].replace('tracker_viewer/index.html', '') + download_url[1].replace('demo=../', '')
        file_dl = download_tracker(download_url)
        data = scraper.parse_data(t)
        save_file(data)
        if file_dl:
            move_trackers(tracker_name)


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
    parse_remote_trackers('2023-05-30', '2023-05-30')
    # parse_local_trackers(LOCAL_TRACKERS_PATH)
