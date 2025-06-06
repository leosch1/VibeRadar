# Vibe Radar API

This is a simple API for the Vibe Radar project, which allows you to get the current state of the radar and update it with new data.

### API Endpoints

Initialize the api with the following command:
```bash
docker-compose up -d
```
This will start the database and API. You can access the API at `http://localhost:8008`.
The full documentation is available at `http://localhost:8008/docs`.

#### `POST /getVibe`
Retrieve the vibe for a given location.

**Request Body**:
```json
{
    "user_ip": "83.79.72.229",
    "lat": 47.3769,
    "lng": 8.5417
}
```

**Response**:
```json
{
    "locationName": "Belém",
    "countryName": "Brasil",
    "lat": 47.3769,
    "long": 8.5417,
    "UtcOffsetSeconds": -10800,
    "weather": {
        "temperatureCelsius": 25,
        "type": "sunny"
    },
    "vibes": {
        "spotify": {
            "playlistId": "djye2ih3fs"
        },
        "youtube": {
            "videoId": "3nYnfYJAkao"
    }
}
```

**Description**:
- `lat` and `lng`: Latitude and longitude of the location.
- `locationName` and `countryName`: Name and country of the location
- `UtcOffsetSeconds`: Timezone offset in seconds.
- `temperatureCelsius`: Current temperature in Celsius.
- `type`: either "cloudy", "sunny", "rainy" or "snowy"
- `playlistId`: ID of the Spotify playlist.


### Build the API with Docker 
```bash
# You can build the API with Docker using the following command:
docker compose up --build

# If the container already exists ensure removing the database volume
docker compose down -v

```
