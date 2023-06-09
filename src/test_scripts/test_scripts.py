import requests
import json


def get_api_key(client_id : str, client_secret : str) -> dict:
    spotify_url = "https://accounts.spotify.com/api/token"
    request_header = {"Content-Type": "application/x-www-form-urlencoded"}
    request_params = {"grant_type": "client_credentials",
                      "client_id": client_id,
                      "client_secret": client_secret}
    api_request = requests.post(spotify_url, headers=request_header, params=request_params)
    return json.loads(api_request.text)
