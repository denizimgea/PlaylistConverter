import os, requests, json
from exceptions import AuthException

API_URL = "https://api.spotify.com/v1/"
API_KEY_URL = "https://accounts.spotify.com/api/token"
AUTH_FILE_DIR = f"{os.getcwd()}\\..\\auth.json"
PLAYLIST_API_URL = f"{API_URL}playlists/"


def send_api_request(request_method: str, request_url: str, request_header: dict = None
                     , request_params: dict = None) -> dict:
    request = requests.request(request_method, request_url, headers=request_header,
                               params=request_params)
    if request.status_code == 200:
        return json.loads(request.text)
    elif request.status_code == 403:
        raise AuthException
    else:
        exit(-1)


def api_key_request(client_id: str, client_secret: str) -> dict:
    request_header = {"Content-Type": "application/x-www-form-urlencoded"}
    request_params = {"grant_type": "client_credentials",
                      "client_id": client_id,
                      "client_secret": client_secret}
    test = send_api_request("POST", API_KEY_URL, request_header, request_params)
    return test


def playlist_to_search_queries(playlist: list):
    return map(lambda x: str.format("{} {}", x["track"]["artists"][0]["name"], x["track"]["name"]),
               playlist)


class SpotifyInteractor:
    _authentication_information: dict

    def __init__(self):
        authentication_file = open(AUTH_FILE_DIR, "r")
        self._authentication_information = json.load(authentication_file)
        authentication_file.close()
        self.update_auth_information()
        if "auth_header" not in self._authentication_information:
            self.update_auth_information()

    def __del__(self):
        authentication_file = open(AUTH_FILE_DIR, "w")
        json.dump(self._authentication_information, authentication_file)
        authentication_file.close()

    def update_auth_information(self):
        new_api_key = api_key_request(self._authentication_information["client_id"],
                                      self._authentication_information["client_secret"])
        self._authentication_information.update(new_api_key)
        self._authentication_information["auth_header"] \
            = str.format("{}  {}", new_api_key["token_type"], new_api_key["access_token"])

    def get_client_id(self):
        return self._authentication_information["client_id"]

    def get_client_secret(self):
        return self._authentication_information["client_secret"]

    def get_api_token_header(self):
        return {"Authorization": self._authentication_information["auth_header"]}

    def get_playlist_data(self, playlist_uri: str) -> dict:
        return send_api_request("GET", f"{PLAYLIST_API_URL}{playlist_uri}",
                                request_header=self.get_api_token_header())

    def get_playlist_tracks(self, playlist_uri) -> list:
        playlist_response = self.get_playlist_data(playlist_uri)["tracks"]
        playlist_tracks = []
        while True:
            playlist_tracks += playlist_response["items"]
            if playlist_response["next"] is None:
                break
            playlist_response = send_api_request("GET", playlist_response["next"]
                                                 , self.get_api_token_header())
        return playlist_tracks

    def _send_api_request(self, request_method: str, request_url: str, request_header: dict = None,
                          request_params: dict = None) -> dict:
        try:
            return send_api_request(request_method, request_url, request_header, request_params)
        except AuthException:
            self.update_auth_information()
            return send_api_request(request_method, request_url, request_header, request_params)

