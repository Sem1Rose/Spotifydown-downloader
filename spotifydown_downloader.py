import unicodedata
import re
import os
import sys
import math
import spotipy

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
from colorama import Fore
from os import listdir
from os.path import isfile, join
from sys import exit
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()


def get_tracks_meta(id):
    tracks_response = sp.playlist_tracks(id) if download_type == 0 else sp.album_tracks(
        id) if download_type == 1 else sp.track(id)

    if download_type == 2:
        return tracks_response

    tracks = tracks_response["items"]
    while tracks_response["next"]:
        tracks_response = sp.next(tracks_response)
        tracks.extend(tracks_response["items"])

    return tracks


def print_help():
    print('\nUsage:\n\tspotify_downloader [options]\n\nOptions:\n\t-h, --help\t\t\tShow help.\n\t-u, --url <url>\t\t\tSets the URL of the playlist/track to be downloaded to <url>.\n\t-o, --output-path <path>\tSet output path to <path>, default is Music directory.\n\t-s, --start-index\t\tSet the download offset (i.e. index of the first song to be downloaded.)\n\t-r, --range\t\tSet the number of tracks to be downloaded from the playlist/album. Can be used with the -s flag to download a portion of the playlist.')


def print_error(error):
    print(f'{Fore.RED}{error}{Fore.WHITE}')
    exit()


def enter_url():
    while len(driver.find_elements(By.CLASS_NAME, 'grid-cols-3')) == 0:
        driver.find_element(By.CLASS_NAME, 'searchInput').send_keys(url)
        driver.find_element(By.CLASS_NAME, 'cursor-pointer').click()
        sleep(2)

    sleep(2)


def refresh():
    driver.get(r'https://spotifydown.com')
    sleep(2)


def get_buttons():
    return driver.find_elements(By.CLASS_NAME, 'cursor-pointer')


def get_current_page_tracks(load_more, page):
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


def remove_invalid_chars(s):
    return re.sub('[^\x00-\x7F]', '_', unicodedata.normalize('NFKD', s.replace('\\', '_').replace('/', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')).encode('ascii', 'ignore').decode('ascii'))


def rename_file(index):
    files = [f for f in listdir(download_path)
             if isfile(join(download_path, f)) and f.endswith('.mp3')]
    for file in files:
        if not file.startswith('spotifydown.com - '):
            continue

        try:
            if download_type == 2:
                artists = ", ".join(
                    [artist["name"] for artist in metadata["artists"]]
                )
                os.rename(join(download_path, file), join(download_path, remove_invalid_chars(
                    f'{artists} - {metadata["name"]}') + '.mp3'))
            else:
                artists = ", ".join(
                    [artist["name"]
                        for artist in metadata[index]["track"]["artists"]]
                )
                os.rename(join(download_path, file), join(download_path, remove_invalid_chars(
                    f'{artists} - {metadata[index]["track"]["name"]}') + '.mp3'))
        except:
            print(
                f'\n{Fore.RED}Counld not rename {Fore.LIGHTRED_EX}{file}{Fore.WHITE}', end='')

        break


sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=os.getenv("CLIENT_ID", ""), client_secret=os.getenv("CLIENT_SECRET", ""))
)

download_path = str(Path.home() / "Music/")
download_type = 0       # 0: playlist, 1: album, 2: track
load_more = False
page = 0
start_index = 0
stop_index = int(9e9)
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
        elif i == 1:
            input = sys.argv[i]
            if not re.match(r'https://open.spotify.com/(.*)', input):
                break

            type = input.split('/')[3]
            if type == 'playlist':
                download_type = 0
            elif type == 'album':
                download_type = 1
            elif type == 'track':
                download_type = 2
            else:
                print_error('Unsupported URL')

            url = input
        elif sys.argv[i] == '-u' or sys.argv[i] == '--url':
            if url != '':
                if i + 1 < len(sys.argv):
                    print_error(
                        f'Multiple URLs were provided: {url}, {sys.argv[i + 1]}')
                else:
                    print_error(
                        f'Can\'t use the {sys.argv[i]} after providing a URL')

            if i + 1 == len(sys.argv):
                print_error(
                    f'Expected playlist URL after the {sys.argv[i]} flag')

            url = sys.argv[i + 1]
            if not re.match(r"https://open.spotify.com/(.*)", url):
                print_error(
                    "Expected URL format: https://open.spotify.com/...")

            type = url.split('/')[3]
            if type == 'playlist':
                download_type = 0
            elif type == 'album':
                download_type = 1
            elif type == 'track':
                download_type = 2
            else:
                print_error('Unsupported URL')

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
                    'Offset must be a positive integer less than the size of the playlist.')

            if offset < -1:
                print_error('Offset must be a positive integer less than the size of the playlist.')
            elif offset == -1:
                offset = 0

            page = math.floor(offset / 100)
            load_more = page > 0
            start_index = offset % 100

            i += 1
        elif sys.argv[i] == '-r' or sys.argv[i] == '--range':
            if i + 1 == len(sys.argv):
                print_error(
                    f'Expected range after the {sys.argv[i]} flag')

            try:
                r = int(sys.argv[i + 1])
            except:
                print_error('Range must be a positive integer.')

            if r < 0:
                print_error(
                    'Range must be a positive integer.')

            stop_index = start_index + r
            i += 1
        else:
            print_error(f'Unknown argument: {sys.argv[i]}')

        i += 1

    if url == '':
        print_error('No URL was provided')
    if download_type == 2:
        if start_index != 0:
            print_error('Can\'t change Offset when downloading a track.')
        if stop_index != int(9e9):
            print_error('Can\'t change Range when donwlaoding a track.')

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option(
        "prefs", {"download.default_directory": download_path, "directory_upgrade": True})

    driver = webdriver.Chrome(options=options)
    driver.minimize_window()

    metadata = get_tracks_meta(url)

    if start_index > len(metadata):
        print_error('Offset was beyond playlist size')
    if stop_index != int(9e9) and stop_index > len(metadata):
        print_error('Range was beyond playlist size')

    print(f'{Fore.GREEN}Downloading {Fore.LIGHTBLUE_EX}{(1 if download_type == 2 else min(stop_index - start_index, len(metadata) - start_index))}{Fore.GREEN} track' +
          ('s' if min(stop_index - start_index, len(metadata) - start_index) > 1 and download_type != 2 else '') + f'{Fore.WHITE}')

    p = 0
    t = 0
    while True:
        tracks = get_current_page_tracks(load_more, page)
        num_tracks = len(tracks)

        stop_index -= p * 100

        for index in range(start_index, min(100, min(num_tracks, stop_index))):
            print(end='\r')
            download_song(get_current_page_tracks(load_more, page)[index])
            print(f'{Fore.CYAN}  - downloaded {Fore.LIGHTBLUE_EX}{t + 1}{Fore.CYAN} track' +
                  (f's{Fore.WHITE}' if t + 1 > 1 else f'{Fore.WHITE}'), end='')
            sleep(.5)
            rename_file(page * 100 + index)
            t += 1

        load_more = num_tracks > 100
        if not load_more:
            break

        start_index = 0
        page += 1
        p += 1

    sleep(1)
    driver.close()
    print(f'\n{Fore.GREEN}Finished{Fore.WHITE}')
