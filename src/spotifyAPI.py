import base64
import json

from dotenv import load_dotenv
import os
import string
import random
from src import playlist

from requests import post, get

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


def get_auth_header(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


def login():
    scope = "playlist-read-private%20user-read-private%20user-read-email"
    state = get_random_string(16)

    redirect_url = 'https://accounts.spotify.com/authorize?' + \
                   f'response_type=code&client_id={client_id}&' + \
                   f'scope={scope}&redirect_uri={redirect_uri}&' + \
                   f'state={state}'

    return redirect_url


def client_auth(code):
    auth_str = f"{client_id}:{client_secret}"
    auth_bytes = auth_str.encode('utf8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        'grant_type': "authorization_code",
        'code': code,
        'redirect_uri': redirect_uri
    }
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.text)
    auth_token = json_result['access_token']
    return auth_token


def get_username(token):
    url = "https://api.spotify.com/v1/me"
    auth_headers = get_auth_header(token)
    result = get(url, headers=auth_headers)
    json_result = json.loads(result.text)
    return json_result['display_name']


def get_playlists(token):
    url = "https://api.spotify.com/v1/me/playlists?limit=50&"
    auth_headers = get_auth_header(token)
    result = get(url, headers=auth_headers)
    json_result = json.loads(result.text)
    playlists = []

    for item in json_result['items']:
        name = item['name']
        id = item['id']
        url = item['external_urls']['spotify']
        owner = item['owner']['display_name']
        playlist_obj = playlist.Playlist(id, name, url, owner)
        playlists.append(playlist_obj)

    return playlists

def get_tracks(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    auth_headers = get_auth_header(token)
    result = get(url, headers=auth_headers)
    json_result = json.loads(result.text)
    tracks = []

    for item in json_result['items']:
        name = item['track']['name']
        id = item['track']['id']
        url = item['track']['external_urls']['spotify']
        artist = item['track']['artists'][0]['name']
        track_obj = playlist.Track(id, name, url, artist)
        tracks.append(track_obj)

    return tracks

