import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="6e101187d7174df0ae6f608b80c792c3",
    client_secret="af258fdc98634027b7e0f47a28b115e7",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-read-private"
))

# Get current user's playlists with their IDs
results = sp.current_user_playlists()
for idx, item in enumerate(results['items']):
    print(f"{idx+1}: {item['name']} --> {item['id']}")


