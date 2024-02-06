<div align=center>

# Spotifydown downloader

Download Spotify playlists and tracks using **[Spotifydown](https://spotifydown.com)**

</div>

## Installation

- Download latest version from the **[Releases Page](https://github.com/Sem1Rose/Spotifydown-downloader/releases)**
- Setup Spotify client credentials:
  - Follow this **[tutorial](https://support.heateor.com/get-spotify-client-id-client-secret/)** to create a new app on your Spotify Dashboard.
  - After getting the Client ID and Client secret, you have two options:
    1. Create a `credentials.env` file:
       - create a new file in the same directory as the script and name it `credentials.env`.
       - Paste the following snippet into the `credentials.env` file:
         ```bash
         CLIENT_ID='[client_id]'
         CLIENT_SECRET='[client_secret]'
         ```
       - Replace `[client_id]` and `[client_secret]` with your Client ID and Client secret.
    2. Change the system environment variables:
       - On your windows machine, open Search and search for `Edit the system environment variables`.
       - Click on `Environment Variables`.
       - In the system variables section, click on `New`.
         - In the Variable name, enter `SPOTIPY_CLIENT_ID`.
         - In the Variable value, enter your Client ID.
       - Repeat the last step again, enter `SPOTIPY_CLIENT_SECRET` for the variable name, and your Client secret for the value.

## Usage

- Basic usage (download playlist/album/track):
  ```bash
  py spotifydown_downloader.py <url>
  ```
- General usage:
  ```bash
  py spotifydown_downloader.py <url> [options]
  ```

<details>
<summary>Available options</summary>

- `-h`, `-help`: Shows help and exits.

- `-o`, `--output-path`: Sets the output path.

  - Usage: `py spotifydown_downloader.py -o <path>`
    > The default download location is **`%USERPROFILE%/Music`** folder (i.e. Current user's music library folder.)

- `-s`, `--start-index`: Set the index of the first song to be downloaded. <sub><sup>**playlist/album only**</sup></sub>

  - Usage: `py spotifydown_downloader.py -s <index>`
    > `index` must be a non-zero positive integer and must not exceed the length of the playlist

- `-r`, `-range`: Set the number of tracks to be downloaded from the playlist/album. <sub><sup>**playlist/album only**</sup></sub>
  - Usage: `py spotifydown_downloader.py -r <range>`
    > `range` must be a non-zero positive integer.

</details>

## Examples

- Download a single track:
  ```bash
  py spotifydown_downloader.py https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT
  ```
- Download a full album:
  ```bash
  py spotifydown_downloader.py https://open.spotify.com/album/6aI0ZE5xJ6GXYx5NOvmxKa
  ```
- Download the first 10 tracks from a playlist:
  ```bash
  py spotifydown_downloader.py https://open.spotify.com/playlist/6CrBHln7J1YeiZPusKbQr8 -r 10
  ```
- Download tracks from 3 to 12 (inclusive) from a playlist:
  ```bash
  py spotifydown_downloader.py https://open.spotify.com/playlist/6CrBHln7J1YeiZPusKbQr8 -s 3 -r 10
  ```
- Download a track to a selected path:
  ```bash
  py spotifydown_downloader.py https://open.spotify.com/track/5ubvP9oKmxLUVq506fgLhk -o "path/to/download/folder"
  ```

> **Note**<br>
> To change the output folder, right-click on the folder and choose _`Copy as path`_, and then paste the copied path after the `-o` flag.

> **Note**<br>
> To get the correct `range` value, use the formula: `final track index - first track index + 1`.<br> > **Example**: To download tracks starting from track number `3` to track number `7`: `7 - 3 + 1 = 5`, so the correct `range` value is `5`.
