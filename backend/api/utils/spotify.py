import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values
import os
import time

# Attention: This code requires a my personal spotify id and secret. 
# Since I don't want to dox myself, I will not provide them here.

class Spotify(spotipy.Spotify):
    def __init__(self):
        # Load environment variables from .env file
        secrets = dotenv_values(os.path.join(os.path.dirname(__file__), ".env"))
        # Set up authentication
        super().__init__(auth_manager=SpotifyOAuth(client_id=secrets['SPOTIFY_CLIENT_ID'],
                                                   client_secret=secrets['SPOTIFY_CLIENT_SECRET'],
                                                   redirect_uri='http://127.0.0.1:8888/callback',
                                                   scope='playlist-modify-public'))

    def create_vibe_playlist(self, location: str):
        """
        Create a new public Spotify playlist with the name of the location.

        Args:
            location (str): The location for which to create the playlist.
        
        Returns:
            dict: The created playlist object.
        """
        user_id = self.current_user()['id']
        playlist = self.user_playlist_create(user=user_id, 
                                             name=f'{location} Vibe',
                                             public=True, 
                                             description=f'A playlist with the most popular songs around {location}')
        
        print(f"Created playlist: {playlist['name']}")

        return playlist

    def search_track(self, query: str):
        """
        Search for a track on Spotify using the provided query.

        Args:
            query (str): The search query for the track.
        
        Returns:
            str: The URI of the found track.
        """
        results = self.search(q=query, type='track', limit=1)
        track = results['tracks']['items']
        
        if not track:
            print("No tracks found.")
            return None

        print(f"Found track: {track[0]['name']} by {track[0]['artists'][0]['name']}")

        return track[0]['uri']


if __name__ == "__main__":
    # Example usage
    sp = Spotify()
    location = 'Test'
    playlist = sp.create_vibe_playlist(location)
    track_uris = [
        "spotify:track:7qiZfU4dY1lWllzX7mPBI3",  # Ed Sheeran – Shape of You
        "spotify:track:6kBXZ8j8IuJeRjb6kV6fol",  # Kanye – Stronger
        "spotify:track:1v7L65Lzy0j0vdpRjJewt1"   # Eminem – Lose Yourself
    ]
    sp.playlist_add_items(playlist_id=playlist["id"], items=track_uris)
    
    for i in range(60):
        print(f"Playlist will be deleted in {60-i} seconds")
        time.sleep(1)

    sp.current_user_unfollow_playlist(playlist_id=playlist["id"])
