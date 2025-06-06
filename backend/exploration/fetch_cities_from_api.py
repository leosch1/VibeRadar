from sys import exit
import pandas as pd
from utils.chartmetric_api import Chartmetric_api

api = Chartmetric_api()

country_codes = ['US', 'JP', 'DE', 'FR', 'GB', 'IT', 'CN', 'BR', 'CA', 'ES',
                 'IN', 'MX', 'NL', 'AU', 'AR', 'KR', 'RU', 'CH', 'TW', 'BE',
                 'SE', 'AT', 'TR', 'DK', 'HK', 'PL', 'NO', 'SA', 'FI', 'GR',
                 'ZA', 'TH', 'PT', 'CO', 'IL', 'VE', 'SG', 'ID', 'EG', 'IE',
                 'CL', 'MY', 'NG', 'PH', 'PE', 'CZ', 'NZ', 'HU', 'UA', 'RO',
                 'AE', 'KZ', 'VN', 'EC', 'SI', 'GT', 'LB', 'LU', 'DO', 'LK',
                 'BG', 'SV', 'LT', 'CR', 'CY', 'KE', 'PA', 'BO', 'PY', 'JO',
                 'LV', 'ZW', 'HN', 'EE', 'KH', 'PG', 'NI', 'MD', 'LA', 'SZ',
                 'MN'
                 ]
cities = []

for i, cc in enumerate(country_codes):
    print(f"fetching cities for {cc} {i/len(country_codes)*100}%")
    res = api.Get(f'/api/cities?country_code={cc}')
    if res.status_code != 200:
        print(f'ERROR: received {res.status_code}')
        exit(1)

    data = res.json()

    for entry in data["obj"]:
        cities.append({
            'city_id': entry['city_id'],
            'city_name': entry['city_name'],
            'country': entry['country'],
            'lat': entry['latitude'],
            'lon': entry['longitude'],
            'population': entry['population']
        })

df = pd.DataFrame(cities)
df = df.sort_values(by=['lat', 'lon'])
df.to_csv('data/cities.csv', index=False)
