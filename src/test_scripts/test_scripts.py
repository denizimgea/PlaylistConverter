import requests
import json


def get_api_key(client_id: str, client_secret: str) -> dict:
    spotify_url = "https://accounts.spotify.com/api/token"
    request_header = {"Content-Type": "application/x-www-form-urlencoded"}
    request_params = {"grant_type": "client_credentials",
                      "client_id": client_id,
                      "client_secret": client_secret}
    api_request = requests.post(spotify_url, headers=request_header, params=request_params)
    return json.loads(api_request.text)


def get_playlist_information(api_key: dict, playlist_uri: str) -> dict:
    spotify_url = f"https://api.spotify.com/v1/playlists/{playlist_uri}"
    request_header = {"Authorization": str.format("{}  {}", api_key["token_type"],
                                                  api_key["access_token"])}
    api_request = requests.get(spotify_url, headers=request_header)
    return json.loads(api_request.text)


def get_playlist_tracks(api_key: dict, playlist_uri: str) -> list:
    spotify_url = f"https://api.spotify.com/v1/playlists/{playlist_uri}"
    request_header = {"Authorization": str.format("{}  {}", api_key["token_type"],
                                                  api_key["access_token"])}
    tracks = []
    api_request = requests.get(spotify_url, headers=request_header)
    playlist_information = json.loads(api_request.text)
    playlist_tracks = playlist_information["tracks"]
    while True:
        tracks = tracks + playlist_tracks["items"]
        if playlist_tracks["next"] is None:
            break
        api_request = requests.get(playlist_tracks["next"], headers=request_header)
        playlist_tracks = json.loads(api_request.text)
    return tracks


def reduce_track_information(track_information: dict) -> str:
    return str.format("{} {}", track_information["track"]["artists"][0]["name"],
                      track_information["track"]["name"])
