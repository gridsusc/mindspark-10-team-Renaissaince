import spotipy
import csv
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(show_dialog = True, client_id="70d38d6792fd47338dcb482fc2aba603",
                                                    client_secret="2c2566a941a3493aa33906cc59f93405",
                                                    redirect_uri="http://localhost:8888/callback",
                                                    scope="user-library-read"))

user = sp.user("lwqh6n22yf8j1esekvl1dghpj")

sad_playlist = sp.playlist("7ABD15iASBIpPP5uJ5awvq")
angry_playlist = sp.playlist("2gWbflBkAo4AtS36JcqMh6")
happy_playlist = sp.playlist("6Qf2sXTjlH3HH30Ijo6AUp")
fearful_playlist = sp.playlist("1vU3YBMMOFSLGa492uKjZu")
calm_playlist = sp.playlist("6gCC8kozvUlLGTzl2YO2MR")

headers = ["id","song","artist","album","popularity","duration", "emotion", "danceability","energy","key","loudness","mode","speechiness","acousticness",
"instrumentalness", "liveness", "valance", "tempo"]
data = []
sad_tracks = sad_playlist['tracks']
angry_tracks = sad_playlist['tracks']
happy_tracks = sad_playlist['tracks']
fearful_tracks = fearful_playlist['tracks']
calm_tracks = calm_playlist['tracks']

ids = []
def get_tracks(results, data, tag):
    for i, item in enumerate(results['items']):
        track = item['track']
        if track:
            if (track["artists"][0]["type"] == "artist" and track["artists"][0]["id"] != None):
                        # data.append([track["id"], track["name"], track["artists"][0]["name"], track["album"]["name"]
                        #     ,track["popularity"], track["duration_ms"],track["album"]["images"][0]["url"]])
                    data.append([track["id"], track["name"], track["artists"][0]["name"], track["album"]["name"]
                                ,track["popularity"], track["duration_ms"], tag])
                    ids.append(track["id"])


get_tracks(sad_tracks, data, "sad")
get_tracks(angry_tracks, data, "angry")
get_tracks(happy_tracks, data, "happy")
get_tracks(fearful_tracks, data, "fearful")
get_tracks(calm_tracks, data, "calm")

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


with open("songs.csv", 'w', encoding="utf-8", newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(headers) 
    csvwriter.writerows(final)
