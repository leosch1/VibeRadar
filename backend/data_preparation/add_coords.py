
# Script to add coordinates to the database

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.utils.location import Geolocation
import psycopg2

conn = psycopg2.connect(dbname="postgres",
                        user="postgres",
                        password="postgres")
loc = Geolocation()

# Get all cities with NULL coordinates
cur = conn.cursor()
cur.execute('SELECT id, city_name, region_code FROM cities WHERE lat IS NULL AND lon IS NULL')
rows = cur.fetchall()

for i, row in enumerate(rows):
    city_id, city_name, region_code = row
    print(f"Processing {city_name}, {region_code}[{i}/{len(rows)}]")
    
    # Get coordinates from geolocation service
    location_data = loc.get_from_name(f"{city_name}, {region_code}")
    
    if location_data:
        lat = location_data["lat"]
        lon = location_data["lon"]
        country_name = location_data["country_name"]
        
        # Update the database with the coordinates
        cur.execute('UPDATE cities SET lat = %s, lon = %s, country_name = %s WHERE id = %s', (lat, lon, country_name, city_id))
        conn.commit()
        print(f"Updated {city_name} with coordinates: ({lat}, {lon})")
    else:
        print(f"Failed to get coordinates for {city_name}")