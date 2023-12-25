import json

import spotifyAPI

def getUser(token):
    url = "https://api.spotify.com/v1/me"
    auth_headers = spotifyAPI.get_auth_header(token)
    result = spotifyAPI.get(url, headers=auth_headers)
    json_result = json.loads(result.text)
    return json_result['display_name']



loginUrl = spotifyAPI.login()
print(loginUrl)
print("enter code: ")
code = input()
print(spotifyAPI.get_username(code))


