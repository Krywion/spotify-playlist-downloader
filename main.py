# spotify playlist downloader
import json
import string
import random

from requests import get, post
from dotenv import load_dotenv
import os
import base64

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


def get_token():
    auth_str = f"{client_id}:{client_secret}"
    auth_bytes = auth_str.encode('utf8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.text)
    auth_token = json_result['access_token']
    return auth_token


def get_auth_header(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


def search_for_artist(auth_token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(auth_token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.text)
    artist = json_result['artists']['items'][0]
    return artist


def login():
    scope = "user-read-private"
    state = get_random_string(16)

    url = "https://accounts.spotify.com/authorize?"
    params = {
        "response_type": "code",
        "client_id": client_id,
        scope: scope,
        "redirect_uri": "http://localhost:8080",
        "state": state
    }
    query = "&".join([f"{key}={value}" for key, value in params.items()])
    query_url = url + query
    print(query_url)

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
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8080"
    }
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.text)
    auth_token = json_result['access_token']
    return auth_token

def get_my_playlists(auth_token):
    url = "https://api.spotify.com/v1/me/playlists"
    headers = get_auth_header(auth_token)
    result = get(url, headers=headers)
    json_result = json.loads(result.text)
    print(json_result)



token = get_token()
login()
code = input("Enter code: ")
my_user_token = client_auth(code)
get_my_playlists(my_user_token)

