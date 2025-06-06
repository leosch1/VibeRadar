import os
import random
import time
import pandas as pd
import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, unquote
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.utils.location import Geolocation



class EveryNoiseScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
        self.driver = webdriver.Chrome(options=chrome_options)
        self.base_url = "https://everynoise.com/everyplace.cgi"

        self.conn = psycopg2.connect(dbname="postgres",
                                  user="postgres",
                                  password="postgres",
                                  host="localhost",
                                  port="5432")
        self.loc = Geolocation()

    def get_note_elements(self):
        self.driver.get(self.base_url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".note a")))
        return self.driver.find_elements(By.CSS_SELECTOR, ".note a")

    def extract_city_country(self, href):
        parsed = urlparse(href)
        query = parse_qs(parsed.query)
        if "root" in query:
            value = unquote(query["root"][0])
            if " " in value:
                city, region_code = value.rsplit(" ", 1)
                return city, region_code
        return None, None

    def get_playlist_id_from_click(self, element):
        try:
            element.click()
            wait = WebDriverWait(self.driver, 15)
            wait.until(EC.presence_of_element_located((By.ID, "spotify")))
            iframe = self.driver.find_element(By.ID, "spotify")
            src = iframe.get_attribute("src")
            parts = src.split(":")
            return parts[-1] if len(parts) >= 3 else None
        except Exception as e:
            print(f"Failed to get playlist ID: {e}")
            return None

    def insert_record(self, record):
        cur = self.conn.cursor()
        try:
            cur.execute(
                'INSERT INTO cities ("city_name", "region_code", "playlist_id", "country", "lat", "lon") VALUES (%s, %s, %s, %s, %s, %s)',
                (record["city"], record["region_code"], record["playlist_id"], record["country"], record["lat"], record["lon"])
            )
            self.conn.commit()
        except Exception as e:
            print(f"Failed to insert record for {record['city']}, {record['region_code']}: {e}")
            self.conn.rollback()

    def get_last_id(self):
        cur = self.conn.cursor()
        cur.execute('SELECT MAX(id) FROM cities')
        result = cur.fetchone()
        return result[0] if result[0] is not None else 0

    def scrape(self):
        print("Loading static city list...")
        note_elements = self.get_note_elements()

        for i in range(self.get_last_id(), len(note_elements)):
            # Reload fresh elements every time to avoid stale references
            self.driver.get(self.base_url)
            note_elements = self.get_note_elements()
            element = note_elements[i]
            href = element.get_attribute("href")
            city, region_code = self.extract_city_country(href)

            if not city or not region_code:
                print(f"Skipping invalid entry at index {i}")
                continue

            # wait for a bit to avoid overwhelming the server
            time.sleep(random.uniform(0.2, 0.7))

            print(f"[{i+1}/{len(note_elements)}] {city}, {region_code} — extracting playlist")
            playlist_id = self.get_playlist_id_from_click(element)

            loc_info = self.loc.get_from_name(f"{city}, {region_code}")
            if loc_info is None:
                print(f"Location info not found for {city}, {region_code}.")
                longitude = None
                latitude = None
            else:
                longitude = loc_info["lon"]
                latitude = loc_info["lat"]
                country = loc_info["country_name"]

            record = {
                "city": city,
                "region_code": region_code,
                "playlist_id": playlist_id,
                "lon": longitude,
                "lat": latitude,
                "country": country
            }

            # Insert record into the "cities" table using the helper function
            self.insert_record(record)

            # wait for a bit to avoid overwhelming the server
            time.sleep(random.uniform(0.2, 0.7))
        print("Done. Data has been written to the database.")


    def close(self):
        self.conn.close()
        self.driver.quit()


if __name__ == "__main__":
    scraper = EveryNoiseScraper()
    try:
        scraper.scrape()
    finally:
        scraper.close()