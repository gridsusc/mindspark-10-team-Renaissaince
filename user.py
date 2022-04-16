import spotipy
import csv
from spotipy.oauth2 import SpotifyOAuth
import pickle
import pandas as pd
import xgboost as xgb
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(show_dialog = True, client_id="70d38d6792fd47338dcb482fc2aba603",
                                                    client_secret="2c2566a941a3493aa33906cc59f93405",
                                                    redirect_uri="http://localhost:8888/callback",
                                                    scope="user-library-read"))

user = sp.user("lwqh6n22yf8j1esekvl1dghpj")

import spotipy
import csv
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(show_dialog = True, client_id="70d38d6792fd47338dcb482fc2aba603",
                                                    client_secret="2c2566a941a3493aa33906cc59f93405",
                                                    redirect_uri="http://localhost:8888/callback",
                                                    scope="user-library-read"))

user = sp.user("lwqh6n22yf8j1esekvl1dghpj")

headers = ["id","song","artist","album","popularity","duration", "danceability","energy","key","loudness","mode","speechiness","acousticness",
"instrumentalness", "liveness", "valance", "tempo","emotion"]

columns = ["id","song","artist","album","popularity","duration", "danceability","energy","key","loudness","mode","speechiness","acousticness",
"instrumentalness", "liveness", "valance", "tempo"]
data = []

ids = []
def get_tracks(results, data):
    for i, item in enumerate(results['items']):
        track = item['track']
        if track:
            if (track["artists"][0]["type"] == "artist" and track["artists"][0]["id"] != None):
                        # data.append([track["id"], track["name"], track["artists"][0]["name"], track["album"]["name"]
                        #     ,track["popularity"], track["duration_ms"],track["album"]["images"][0]["url"]])
                    data.append([track["id"], track["name"], track["artists"][0]["name"], track["album"]["name"]
                                ,track["popularity"], track["duration_ms"]])
                    ids.append(track["id"])


first_user_playlists = sp.user_playlists("lwqh6n22yf8j1esekvl1dghpj")

first_user_playlists_ids = []

print("Scraping first user's playlists\n")
for i, playlist in enumerate(first_user_playlists['items']):
    first_user_playlists_ids.append(playlist['id'])

for playlistId in first_user_playlists_ids:
    results = sp.playlist(playlistId, fields="tracks,next")
    tracks = results['tracks']
    get_tracks(tracks, data)

    while tracks['next']:
        tracks = sp.next(tracks)
        get_tracks(tracks, data)

audio_features = []

for i in range(0, len(ids), 100):
    chunk = ids[i:i+100]
    features = sp.audio_features(chunk)
    for feature in features:
        if (feature is not None):
            audio_features.append([feature["id"], feature["danceability"], feature["energy"], feature["key"],
            feature["loudness"], feature["mode"], feature["speechiness"], feature["acousticness"], 
            feature["instrumentalness"], feature["liveness"], feature["valence"], feature["tempo"]])
i = 0
final = []
for line in data:
    print(audio_features[i][1:])
    line = line + audio_features[i][1:]
    final.append(line)
    i = i + 1

loaded_model = pickle.load(open("rfc.sav", 'rb'))
X = pd.DataFrame(final, columns = columns)


X = X[["energy", "liveness", "tempo", "speechiness","acousticness","instrumentalness","danceability", "loudness","valance"]]
result = loaded_model.predict(X)

final_2 = []
i = 0
for line in final:
    line.append(result[i])
    final_2.append(line)
    print(line)
    i = i + 1

with open("songs.csv", 'w', encoding="utf-8", newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(headers) 
    csvwriter.writerows(final_2)

