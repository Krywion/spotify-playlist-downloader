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
    print("auth_token", auth_token)
    return {"Authorization": f"Bearer {auth_token}"}

def login():
    scope = "user-read-private"
    state = get_random_string(16)

    url = "https://accounts.spotify.com/authorize?"
    params = {
        "response_type": "code",
        "client_id": client_id,
        scope: scope,
        "redirect_uri": "http://localhost:8080/callback",
        "state": state
    }
    query = "&".join([f"{key}={value}" for key, value in params.items()])
    query_url = url + query
    return query_url

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
        'grant_type' : "authorization_code",
        'code' : code,
        'redirect_uri' : "http://localhost:8080/callback"
    }
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.text)
    print(json_result)
    auth_token = json_result['access_token']
    return auth_token

def get_username(code):
    token = client_auth(code)
    url = "https://api.spotify.com/v1/me"
    auth_headers = get_auth_header(token)
    result = get(url, headers=auth_headers)
    json_result = json.loads(result.text)
    print(json_result)
    return json_result['display_name']