# import os

# import spotipy
# from dotenv import load_dotenv
# from spotipy.oauth2 import SpotifyClientCredentials

# load_dotenv()

# CLIENT_ID = os.getenv("CLIENT_ID", "")
# CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
# OUTPUT_FILE_NAME = "track_info.csv"

# session = spotipy.Spotify(
#     client_credentials_manager= SpotifyClientCredentials(
#                             client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
# )

# PLAYLIST_LINK = input('enter playlist URL: ')
# if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
#     playlist_uri = match.groups()[0]
# else:
#     raise ValueError("Expected format: https://open.spotify.com/playlist/...")

# tracks = session.playlist_tracks(playlist_uri, limit=100)["items"]

# for track in tracks:
#     name = track["track"]["name"]
#     artists = ", ".join(
#         [artist["name"] for artist in track["track"]["artists"]]
#     )

#     print(f'{name} - {artists}')


import re
import os
import sys
import math

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
from colorama import Fore
from os import listdir
from os.path import isfile, join
from sys import exit


def print_help():
    print('\nUsage:\n\tspotify_downloader [options]\n\nOptions:\n\t-h, --help\t\t\tShow help.\n\t-u, --URL\t\tSets the URL of the playlist to be downloaded.\n\t-o, --output-path <path>\tSet output path to <path>, default is Music directory.\n\t-s, --start-index\t\tSet download offset, i.e. index of the first song to be downloaded.\n')


def print_error(error):
    print(f'{Fore.RED}{error}{Fore.WHITE}')
    exit()


def enter_url():
    while len(driver.find_elements(By.CLASS_NAME, 'grid-cols-3')) == 0:
        driver.find_element(By.CLASS_NAME, 'searchInput').send_keys(url)
        driver.find_element(By.CLASS_NAME, 'cursor-pointer').click()
        sleep(.3)

    sleep(2)


def refresh():
    driver.get(r'https://spotifydown.com')
    sleep(2)


def get_buttons():
    return driver.find_elements(By.CLASS_NAME, 'cursor-pointer')


def get_songs(load_more, page):
    refresh()
    enter_url()

    if load_more:
        for _ in range(page):
            if len(get_buttons()) <= 100:
                print_error('Offset was beyond playlist size')

            get_buttons()[-1].click()
            sleep(1)
            while len(driver.find_elements(By.CLASS_NAME, 'grid-cols-3')) == 0:
                continue

            sleep(2)

    return get_buttons()


def download_song(download_button):
    download_button.click()

    while len(get_buttons()) != 2:
        continue

    get_buttons()[0].click()
    sleep(2)


download_path = str(Path.home() / "Music/")
load_more = False
page = 0
start_index = 0
url = ''
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print_help()
        exit()

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '-h' or sys.argv[i] == '--help':
            if i + 1 != len(sys.argv):
                print_error(
                    f'{sys.argv[i]} flag doesn\'t accept any arguments!')

            print_help()
            exit()
        elif sys.argv[i] == '-u' or sys.argv[i] == '--URL':
            if i + 1 == len(sys.argv):
                print_error(
                    f'Expected playlist URL after the {sys.argv[i]} flag')

            url = sys.argv[i + 1]
            if not re.match(r"https://open.spotify.com/(.*)", url):
                print_error(
                    "Expected URL format: https://open.spotify.com/...")

            i += 1
        elif sys.argv[i] == '-o' or sys.argv[i] == '--output-path':
            if i + 1 == len(sys.argv):
                print_error(
                    f'Expected download path after the {sys.argv[i]} flag')

            download_path = f'{sys.argv[i + 1]}\\'
            i += 1
        elif sys.argv[i] == '-s' or sys.argv[i] == '--start-index':
            if i + 1 == len(sys.argv):
                print_error(
                    f'Expected start index after the {sys.argv[i]} flag')

            try:
                offset = int(sys.argv[i + 1]) - 1
            except:
                print_error(
                    'Offset must be a positive integer less than the size of the playlist')

            page = math.floor(offset / 100)
            load_more = page > 0
            start_index = offset % 100

            i += 1
        else:
            print_error(f'Unknown argument: {sys.argv[i]}')

        i += 1

    if url == '':
        print_error('No URL was provided')

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option(
        "prefs", {"download.default_directory": download_path, "directory_upgrade": True})

    driver = webdriver.Chrome(options=options)
    driver.minimize_window()

    while True:
        songs = get_songs(load_more, page)
        num_songs = len(songs)
        print(
            f'{Fore.CYAN}Downloading {Fore.MAGENTA}{min(100, num_songs)}{Fore.CYAN} songs, page {Fore.BLUE}{page + 1}{Fore.WHITE}')

        if start_index >= num_songs:
            print_error('Offset was beyond playlist size')

        for index in range(start_index, min(100, num_songs)):
            download_song(get_songs(load_more, page)[index])
            print(
                f'{Fore.MAGENTA}{index + 1}{Fore.CYAN} songs downloaded!{Fore.WHITE}')

        load_more = num_songs > 100
        if not load_more:
            break

        page += 1

    files = [f for f in listdir(download_path)
             if isfile(join(download_path, f))]
    for file in files:
        os.replace(join(download_path, file), join(
            download_path, file.replace('spotifydown.com - ', '')))
