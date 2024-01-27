<div align=center>

# Spotifydown downloader

Download Spotify playlists and tracks using **[Spotifydown](spotifydown.com)**

</div>

## Installation

- Download latest version from the **[Releases Page](https://github.com/Sem1Rose/Spotifydown-downloader/releases)**
- Setup Spotify client credentials:
  - Follow this **[tutorial](https://support.heateor.com/get-spotify-client-id-client-secret/)** to create a new app on your Spotify Dashboard.
  - After getting the Client ID and Client secret, create a new file in the same directory as the script and name it `credentials.env`.
  - Paste the following snippet into the `credentials.env` file:
  ```bash
  CLIENT_ID='[client_id]'
  CLIENT_SECRET='[client_secret]'
  ```
  - Replace `[client_id]` and `[client_secret]` with your Client ID and Client secret.

## Usage

- Basic usage (download playlist/album/track):
  ```bash
  spotifydown_downloader.py [url]
  ```
- General usage:
    ```bash
    spotifydown_downloader.py [options]
    ```
<details>
<summary>Available options</summary>

- `-h`, `-help`: Show help.

- `-u`, `--url`: Sets the URL of the playlist/track to be downloaded. <sub><sup>**required**</sup></sub>

  - Usage: `spotifydown_downloader.py -u <url>`

- `-o`, `--output-path`: Sets the output path.

  - Usage: `spotifydown_downloader.py -o <path>`
    > The default download location is **`%USERPROFILE%/Music`** folder (i.e. Current user's music library folder.)

- `-s`, `--start-index`: Set the download offset (i.e. index of the first song to be downloaded.) <sub><sup>**playlist only**</sup></sub>

  - Usage: `spotifydown_downloader.py -s <offset>`
    > `offset` must be a positive integer and must not exceed the length of the playlist

- `-r`, `-range`: Set the number of tracks to be downloaded from the playlist/album. 
    - Usage: `spotifydown_downloader.py -r <range>` 
        > `range` must be a positive integer.
</details>

## Example
- Download a single track:
    ```bash
    spotifydown_downloader.py https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT
    ```
- Download an album:
    ```bash
    spotifydown_downloader.py https://open.spotify.com/album/6aI0ZE5xJ6GXYx5NOvmxKa
    ```
- Download the first 10 tracks from a playlist:
    ```bash
    spotifydown_downloader.py https://open.spotify.com/playlist/6CrBHln7J1YeiZPusKbQr8 -r 10
    ```
- Download tracks from 3-12 (inclusive) from a playlist:
    ```bash
    spotifydown_downloader.py https://open.spotify.com/playlist/6CrBHln7J1YeiZPusKbQr8 -r 10
    ```
- Download a track to a selected path:
    ```bash
    spotifydown_downloader.py https://open.spotify.com/track/5ubvP9oKmxLUVq506fgLhk -o "path/to/download/folder"
    ```
> **Note**<br>
> To change the output folder, right-click on the folder and choose *`Copy as path`*, and then paste the copied path after the `-o` flag.