import requests

import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
USER_ID = "" #username
TOKEN = "" #generated token

if __name__ == "__main__":
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }

    #retrieve playlists of users
    r = requests.get(
        "https://api.spotify.com/v1/me/playlists",
        headers=headers)

    data = r.json()
    #print(data)

    #convert to json to dataframe
    playlist_name = []
    owner_list = []
    total = []

    for playlist in data['items']:
        playlist_name.append(playlist['name'])
        owner_list.append(playlist['owner']['display_name'])

    playlist_dict = {
        "playlist_name": playlist_name,
        "owner_list": owner_list}

    playlist_df = pd.DataFrame(playlist_dict, columns=["playlist_name", "owner_list"])

    print(playlist_df)

    def check_if_valid_data(df: pd.DataFrame) -> bool:
        #Check if dataframe is empty
        if df.empty:
            print("No playlists are available in spotify account")
            return False

        # Check for nulls
        if df.isnull().values.any():
            raise Exception("Null values found")

        return True







