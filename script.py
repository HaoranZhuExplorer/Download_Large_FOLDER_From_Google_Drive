# downloading large files from google drive in terminal
# use the 2TB ONCE dataset as an example: https://once-for-auto-driving.github.io/download.html

import requests
import subprocess
from typing import Dict


# set your google drive access token. example: https://stackoverflow.com/questions/65312867/how-to-download-large-file-from-google-drive-from-terminal-gdown-doesnt-work



ACCESS_TOKEN = <insert_your_access_token>

# set all the folders and their corresponding id in google drive, for example below:
FOLDERS = {
    "lidar_p3": "1dEqJ_suuYbB2vbSwO8Kw__rNBBKfJ5qJ",
    "lidar_p4": "1qgiTZwV9XIa_UUodSuL17QWkpFfgn9-l",
    "lidar_p5": "19hCy7N7n2YIM_P-K0e5hKCv9-L0G8BRJ",
    "lidar_p6": "1jCXmeddekH3ynF7IRLIe2DYXVZUcUhbw",
    "lidar_p7": "1pD7ayCIkPLpNaK2SyEHUNxp6026z6a0k",
    "lidar_p8": "1zKTUWJ6n8BA9wvLneDmO-Q14vw6xWMCj",
    "lidar_p9": "14FoWbvDmwHeCKfYMNtOlIbNdoBogIrSZ",
}



def list_files_in_folder(access_token: str, folder_id: str) -> dict[str, str]:
    url = "https://www.googleapis.com/drive/v3/files"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "q": f"'{folder_id}' in parents",        # filter by parent folder
        "fields": "nextPageToken, files(id, name)",
        "pageSize": 1000
    }

    file_dict = {}
    while True:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()

        # build map name → id
        for f in data.get("files", []):
            file_dict[f["name"]] = f["id"]

        # page through if necessary
        if token := data.get("nextPageToken"):
            params["pageToken"] = token
        else:
            break

    return file_dict

if __name__ == "__main__":
    for FOLDER_NAME in FOLDERS:
      FOLDER_ID = FOLDERS[FOLDER_NAME]
      print("folder", FOLDER_NAME, FOLDER_ID)
      files = list_files_in_folder(ACCESS_TOKEN, FOLDER_ID)
      for name, fid in files.items():
        print(f"{name}: {fid}")
        if name == "raw_lidar_p3.tar.partaf" or name=="raw_lidar_p3.tar.partae":
            continue
        
        download_command = "curl -H \"Authorization: Bearer {}\" https://www.googleapis.com/drive/v3/files/{}?alt=media -o {}".format(ACCESS_TOKEN, fid, name)
        print(download_command)
        # execute it in linux
        result = subprocess.run(download_command, shell=True, check=True, text=True, stdout=subprocess.PIPE)
