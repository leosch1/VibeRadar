import psycopg2
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.utils.youtube_api import YoutubeAPI 

# Database connection parameters
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

yt_api = YoutubeAPI()

def update_youtube_links():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()

    # Select rows that need YouTube links (adjust table/column names as needed)
    cur.execute("SELECT id, city_name, country_name FROM cities WHERE video_id IS NULL AND active;")
    rows = cur.fetchall()

    for row in rows:
        row_id, city_name, country_name = row
        link = yt_api.get_video_url_from_city(city_name, country_name)
        video_id = link.split("?v=")[-1] if link else None
        if video_id:
            cur.execute(
                f"UPDATE cities SET video_id = '{video_id}' WHERE id = {row_id};"
            )
            print(f"Updated city {city_name} with YouTube link: {video_id}")
        conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    update_youtube_links()