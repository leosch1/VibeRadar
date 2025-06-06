import os
from dotenv import load_dotenv
import requests

# ─── Configuration ────────────────────────────────────────
load_dotenv()
API_KEY = os.getenv('LASTFM_API_KEY')
if not API_KEY:
    raise RuntimeError("Please set LASTFM_API_KEY in your .env file")

BASE_URL = 'http://ws.audioscrobbler.com/2.0/'

# ─── Function ─────────────────────────────────────────────
def get_top_tracks_by_city(
    country: str,
    city:    str,
    limit:   int = 10,
    page:    int = 1
) -> dict:
    """
    Fetch last week’s top tracks for a given city.
    Returns JSON with each track’s 'listeners' count (not playcount).
    """
    params = {
        'method':   'geo.getTopTracks',
        'country':  country,
        'location': city,
        'limit':    limit,
        'page':     page,
        'api_key':  API_KEY,
        'format':   'json'
    }

    with requests.Session() as session:
        resp = session.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()


# ─── Example Usage ────────────────────────────────────────
if __name__ == '__main__':
    country = 'france'
    city    = 'bern' # this parameter is useless because it is never used
    data    = get_top_tracks_by_city(country, city, limit=5)

    tracks = data.get('tracks', {}).get('track', [])
    print(f"Top {len(tracks)} tracks in {city.title()}, {country.title()} (last week):")
    for i, t in enumerate(tracks, start=1):
        artist    = t['artist']['name']
        title     = t['name']
        # geo.getTopTracks returns 'listeners', not 'playcount'
        listeners = t.get('listeners', 'N/A')
        print(f"{i}. {artist} — {title} ({listeners} listeners)")
