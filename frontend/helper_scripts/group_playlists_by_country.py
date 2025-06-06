import json
import re
from collections import defaultdict
from difflib import get_close_matches
import os
import urllib.request

# --- Setup paths ---
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "spotify_owned_playlists.json")
output_path = os.path.join(script_dir, "spotify_owned_playlists_grouped.json")

# --- Download country data with coordinates ---
country_data_url = "https://raw.githubusercontent.com/mledoze/countries/master/countries.json"
with urllib.request.urlopen(country_data_url) as url:
    country_json = json.loads(url.read().decode())

# Create lookup: alpha2 -> {"lat": ..., "lng": ...}
country_code_to_coords = {}
country_name_to_code = {}



for entry in country_json:
    code = entry["cca2"]
    name = entry["name"]["common"]
    latlng = entry["latlng"]
    if latlng:
        country_code_to_coords[code] = {"lat": latlng[0], "lng": latlng[1]}
    country_name_to_code[name] = code

# Add some aliases (manual additions for fuzzy names)
alias_map = {
    "Global": "GLOBAL", "Italia": "IT", "Deutschland": "DE", "España": "ES", "Naija": "NG",
    "Schwiizrap": "CH", "BE": "BE", "NL": "NL", "Delhi": "IN", "La República Dominicana": "DO",
    "Top Dalok": "HU", "Hot Hits BE": "BE", "Hot Hits NL": "NL"
}

# Normalize text
def normalize(text):
    return re.sub(r"[^\w\s]", "", text).lower()

normalized_country_name_map = {normalize(name): code for name, code in country_name_to_code.items()}
normalized_aliases = {normalize(k): v for k, v in alias_map.items()}

# --- Load playlists ---
with open(file_path, "r", encoding="utf-8") as f:
    playlists = json.load(f)

# --- Group playlists ---
grouped = defaultdict(lambda: {"lat": None, "lng": None, "playlists": []})

for item in playlists:
    name = item["playlist_name"]
    code = None

    # Check aliases
    for alias, alias_code in alias_map.items():
        if alias.lower() in name.lower():
            code = alias_code
            break

    # Direct country name match
    if not code:
        for country_name, iso in country_name_to_code.items():
            if country_name.lower() in name.lower():
                code = iso
                break

    # Fuzzy fallback
    if not code:
        words = re.findall(r"\w+", name)
        for word in words:
            match = get_close_matches(normalize(word), normalized_country_name_map.keys(), n=1, cutoff=0.9)
            if match:
                code = normalized_country_name_map[match[0]]
                break

    if not code:
        code = "Other"

    # Assign coordinates if known
    if code != "Other" and code in country_code_to_coords:
        grouped[code]["lat"] = country_code_to_coords[code]["lat"]
        grouped[code]["lng"] = country_code_to_coords[code]["lng"]

    grouped[code]["playlists"].append(item)

# --- Write output ---
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(grouped, f, ensure_ascii=False, indent=2)

print(f"Grouped playlists written to {output_path}")
