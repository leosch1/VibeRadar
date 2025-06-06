
import os
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
from utils.weather import Weather
# from utils.spotify import Spotify
from utils.posthog_api import PostHogAPI
from utils.location import Geolocation
from utils.database_operations import DatabaseOperations
import time
import subprocess

# Use environment variable, fallback to local default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
DATABASE_SEED_FILE = "sql/02_backup.sql"

# database to be started
time.sleep(5)

# drop database if it exists
subprocess.run(
    ["psql", f"--dbname={DATABASE_URL}", "-c", "DROP SCHEMA IF EXISTS public CASCADE;"],
    check=True
)

# create database
subprocess.run(
    ["psql", f"--dbname={DATABASE_URL}", "-c", "CREATE SCHEMA public;"],
    check=True
)

# seeding database befor running the app
res = subprocess.run(
["psql", f"--dbname={DATABASE_URL}", "-c", "CREATE EXTENSION IF NOT EXISTS postgis;"],
check=True
)
if os.path.isfile(DATABASE_SEED_FILE):
    command = ["psql", f"--dbname={DATABASE_URL}", "-f", DATABASE_SEED_FILE]
    subprocess.run(command, check=True)
else:
    raise FileNotFoundError("Database seed file not found.")

# wait for the seeding to be completed
time.sleep(5)

weather = Weather()
geolocation = Geolocation()
dbo = DatabaseOperations(db_url=DATABASE_URL)
posthog = PostHogAPI()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Geoposition(BaseModel):
    lat: float
    lng: float

class Connection(BaseModel):
    start: Geoposition
    end: Geoposition

class ConnectionRequest(BaseModel):
    sessionId: str
    myConnection: Connection | None = None

class WeatherOut(BaseModel):
    temperatureCelsius: int
    type: Literal["cloudy", "sunny", "rainy", "snowy"]

class SpotifyVibe(BaseModel):
    playlistId: str

class YoutubeVibe(BaseModel):
    videoId: str

class Vibes(BaseModel):
    spotify: SpotifyVibe
    youtube: YoutubeVibe

class VibeResponse(BaseModel):
    locationName: str
    countryName: str
    lat: float
    lng: float
    utcOffsetSeconds: int
    weather: WeatherOut
    vibes: Vibes

class ConnectionsResponse(BaseModel):
    connections: list[Connection]

@app.post("/getVibe", response_model=VibeResponse)
def get_vibe(location: Geoposition):
    weather_data = weather.get_from_coords(location.lat, location.lng)
    # location_data = geolocation.get_from_coords(location.lat, location.lng)
    data = dbo.get_nearest_playlist2((location.lat, location.lng))

    return {
        "locationName": data["city_name"],
        "countryName": data["country_name"],
        "lat": data["lat"],
        "lng": data["lon"],
        "utcOffsetSeconds": weather_data["utcOffsetSeconds"],
        "weather": weather_data["weather"],
        "vibes": {
            "spotify": {
                "playlistId": data["playlist_id"]
            },
            "youtube": {
                "videoId": data["video_id"]
            }   
        }
    }

@app.post("/getOtherConnections", response_model=ConnectionsResponse)
def get_connections(req: ConnectionRequest):
    connections = dbo.get_other_connections(req)
    return {
        "connections": connections
    }

@app.get("/health")
def get_health():
    # Check if the database is reachable
    if dbo.check_db_health():
        return Response(status_code=200, content="OK")
    else:
        # If there's an error, return a 500 response
        return Response(status_code=500, content="Database connection error")

@app.get("/metrics/this-weeks-users", response_model=None)
def get_this_weeks_users():
    return posthog.get_this_weeks_users()

@app.get("/metrics/avg-session-duration", response_model=None)
def get_avg_session_duration():
    return posthog.get_avg_session_duration()

@app.get("/metrics/top-city", response_model=None)
def get_top_city():
    return posthog.get_top_city()