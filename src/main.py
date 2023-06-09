from spotify_interaction import SpotifyInteractor, playlist_to_search_queries

def main():
    interactor = SpotifyInteractor()
    test1 = interactor.get_playlist_tracks(playlist_uri="5IoImA8q1y4a0Kir7wUeMV")
    search_queries = list(playlist_to_search_queries(test1))
    pass


if __name__ == "__main__":
    main()
