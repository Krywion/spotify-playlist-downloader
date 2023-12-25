import base64
import json

from dotenv import load_dotenv
import os
import string
import random

from requests import post, get

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


def get_auth_header(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


def login():
    scope = "playlist-read-private%20user-read-private%20user-read-email"
    state = get_random_string(16)


    redirect_uri = "http://localhost:8080/callback"
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
        'redirect_uri': "http://localhost:8080/callback"
    }
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.text)
    print(json_result)
    auth_token = json_result['access_token']
    return auth_token


def get_username(token):
    url = "https://api.spotify.com/v1/me"
    auth_headers = get_auth_header(token)
    print(auth_headers)
    result = get(url, headers=auth_headers)
    json_result = json.loads(result.text)
    return json_result['display_name']


def get_playlists(token):
    url = "https://api.spotify.com/v1/me/playlists?limit=50&"
    auth_headers = get_auth_header(token)
    result = get(url, headers=auth_headers)
    json_result = json.loads(result.text)
    print(json_result)
    playlists = []
    for item in json_result['items']:
        playlists.append(item['name'])
    return playlists
