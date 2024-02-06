import unicodedata
import re
import os
import math
import spotipy
import argparse
import sys

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
from colorama import Fore
from os import listdir
from os.path import isfile, exists, join
from sys import exit
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials


if getattr(sys, 'frozen', False):
    load_dotenv(os.path.join(sys._MEIPASS, "credentials.env"))
else:
    load_dotenv("credentials.env")


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


def parse_args():
    parser = argparse.ArgumentParser(
        description='Download Spotify playlists and tracks using Spotifydown.com', usage='%(prog)s <url> [options]')

    parser.add_argument(
        'url', help='URL of the playlist/album/track to be downloaded.')
    parser.add_argument('-o', '--output-path', dest='path', default=str(
        Path.home() / "Music/"), help='Sets the output path to <PATH>.')
    parser.add_argument('-s', '--start-index', dest='index', type=int,
                        help='Set the index of the first song to be downloaded to <INDEX>.')
    parser.add_argument('-r', '--range', type=int,
                        help='Set the number of tracks to be downloaded from the playlist/album to <RANGE>.')

    return parser.parse_args()


def process_args(args):
    if not exists(args.path):
        print_error('Path doesn\'t exist: ', args.path, '.')

    if args.index is not None and args.index < 1:
        print_error('Start index must be a non-zero positive integer!')

    if args.range is not None and args.range < 1:
        print_error('Range must be a non-zero positive integer!')

    if not re.match(r"https://open.spotify.com/(.*)", args.url):
        print_error("Expected URL format: https://open.spotify.com/...")

    return args


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--log-level=3")
    options.add_experimental_option(
        "prefs", {"download.default_directory": download_path, "directory_upgrade": True})

    return webdriver.Chrome(options=options)


def print_error(*error):
    print(f'{Fore.RED}', ''.join(error), f'{Fore.WHITE}')
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
                print_error('Start index was beyond playlist size')

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


def replace(str: str, strs: str, replace_with: str):
    for i in strs:
        str = str.replace(i, replace_with)

    return str


def remove_invalid_chars(s) -> str:
    return re.sub('[^\x00-\x7F]', '_', unicodedata.normalize('NFKD', replace(s, '\/:*?"<>|', '_')).encode('ascii', 'ignore').decode('ascii'))


def get_track_name(index=0) -> str:
    if download_type == 2:
        artists = ", ".join(
            [artist["name"]
             for artist in metadata["artists"]]
        )
        name = metadata["name"]

    else:
        artists = ", ".join(
            [artist["name"]
             for artist in metadata[index]["track"]["artists"]]
        )
        name = metadata[index]["track"]["name"]

    return remove_invalid_chars(f"{artists} - {name}")


def check_track_exists(index):
    name = get_track_name(index) + '.mp3'
    return exists(join(download_path, name))


def rename_file(index):
    files = [f for f in listdir(download_path)
             if isfile(join(download_path, f)) and f.endswith('.mp3')]
    for file in files:
        if not file.startswith('spotifydown.com - '):
            continue

        try:
            if download_type == 2:
                os.replace(join(download_path, file), join(
                    download_path, get_track_name() + '.mp3'))
            else:
                os.replace(join(download_path, file), join(
                    download_path, get_track_name(index) + '.mp3'))
        except:
            print(
                f'\n{Fore.RED}Counld not rename {Fore.LIGHTRED_EX}{file}{Fore.WHITE}', end='')

        break


if __name__ == '__main__':
    args = process_args(parse_args())

    url = args.url

    index = args.index - 1 if args.index is not None else 0
    page = math.floor(index / 100)
    load_more = page > 0
    start_index = index % 100

    if args.range is not None:
        stop_index = index + args.range
    else:
        stop_index = int(9e9)

    download_path = f'{args.path}\\'

    type = url.split('/')[3]
    if type == 'playlist':
        download_type = 0
    elif type == 'album':
        download_type = 1
    elif type == 'track':
        download_type = 2
    else:
        print_error('Unsupported URL')

    if download_type == 2:
        if start_index is not None:
            print_error('Can\'t change Start index when downloading a track.')
        if args.range is not None:
            print_error('Can\'t change Range when donwlaoding a track.')

    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=os.getenv("CLIENT_ID", ""), client_secret=os.getenv("CLIENT_SECRET", "")))

    driver = init_driver()
    print('\033[F\033[K\033[F', end='\r')

    metadata = get_tracks_meta(url)
    if start_index > len(metadata) - 1:
        print_error('Start index was beyond playlist size')
    if args.range is not None and stop_index > len(metadata):
        print_error('Range was beyond playlist size')

    print(f'{Fore.GREEN}Downloading {Fore.LIGHTBLUE_EX}{(1 if download_type == 2 else min(stop_index - start_index, len(metadata) - start_index))}{Fore.GREEN} track' +
          (f's{Fore.WHITE}' if download_type != 2 and min(stop_index - start_index, len(metadata) - start_index) > 1 else f'{Fore.WHITE}'), end='\n\n')

    p = 0
    t = 0
    while True:
        tracks = get_current_page_tracks(load_more, page)
        num_tracks = len(tracks)

        stop_index -= p * 100

        for index in range(start_index, min(100, min(num_tracks, stop_index))):
            if not check_track_exists(index):
                download_song(get_current_page_tracks(load_more, page)[index])
                sleep(.5)
                rename_file(page * 100 + index)

            print('\r\033[F\033[F\r')
            print(f'{Fore.CYAN}' + ' ' * 100 + f'\r  - downloaded {Fore.LIGHTBLUE_EX}{t + 1}{Fore.CYAN} track' +
                  (f's{Fore.WHITE}' if t + 1 > 1 else f'{Fore.WHITE}'))
            print(
                f'{Fore.CYAN}' + ' ' * 100 + f'\r  - downloaded {Fore.LIGHTBLUE_EX}{get_track_name(index)}{Fore.WHITE}', end='')

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
