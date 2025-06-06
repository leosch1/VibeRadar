from bs4 import BeautifulSoup
import json
import re
import os

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(script_dir, "spotify_playlist_search.html")

# Load the local HTML file
with open(html_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

playlist_cards = soup.find_all("div", class_="Card")

results = []

for card in playlist_cards:
    subtitle_div = card.find("div", class_="CardDetails__CardDetailText-sc-1gdonml-1")
    if subtitle_div and "By Spotify" in subtitle_div.text:
        title_element = card.find("p", {"data-encore-id": "cardTitle"})
        link_element = card.find("a", href=True)

        if title_element and link_element:
            raw_name = title_element.get_text()
            playlist_name = clean_text(raw_name)
            playlist_link = link_element["href"].strip()
            results.append({
                "playlist_name": playlist_name,
                "link": playlist_link
            })

# Output as JSON
json_output = json.dumps(results, indent=4, ensure_ascii=False)

# Write to file spotify_owned_playlists.json in the same directory
output_path = os.path.join(script_dir, "spotify_owned_playlists.json")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(json_output)

print(f"Spotify owned playlists have been written to {output_path}")
