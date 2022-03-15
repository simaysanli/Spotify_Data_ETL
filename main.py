import requests

import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite:///my_played_list.sqlite"
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
    playlist_id = []

    for playlist in data['items']:
        playlist_name.append(playlist['name'])
        owner_list.append(playlist['owner']['display_name'])
        playlist_id.append(playlist['id'])

    playlist_dict = {
        "playlist_name": playlist_name,
        "owner_list": owner_list,
        "ID": playlist_id}

    playlist_df = pd.DataFrame(playlist_dict, columns=["ID","playlist_name", "owner_list"])

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

    #Validate
    if check_if_valid_data(playlist_df):
        print("Data is valid, can be proceeded to Load stage")


    #Load

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    connection = sqlite3.connect('my_played_list.sqlite')
    cursor = connection.cursor()

    sql_query = """
        CREATE TABLE IF NOT EXISTS my_played_list(
            playlist_name VARCHAR(200),
            owner_name VARCHAR(200),
            ID VARCHAR(200),
            CONSTRAINT primary_key_constraint PRIMARY KEY (ID)
        )
        """

    cursor.execute(sql_query)
    print("Opened database successfully")

    try:
        playlist_df.to_sql("my_played_list", engine, index=False, if_exists='append')
    except:
        print("Data already exists in database")

    connection.close()
    print("Closed database successfully")
            
    









