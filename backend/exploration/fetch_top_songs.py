from sys import exit
from utils.chartmetric_api import Chartmetric_api

api = Chartmetric_api()
entities = ['youtube', 'shazam', 'radio']
results = []

for e in entities:
    res = api.Get(f'/api/city/545413/{e}/top-tracks') # try 15981
    if res.status_code != 200:
        print(f'ERROR: received {res.status_code}')
        exit(1)

    data = res.json()
    for entry in data["obj"]:
        artist = 'unknown'
        song = 'unknown'
        if 'artist_names' in entry.keys():
            artist = entry['artist_names']
        if 'name' in entry.keys():
            song = entry['name']
        results.append([artist, song])
        

print(results)