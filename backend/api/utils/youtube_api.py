
from youtubesearchpython import VideosSearch

class YoutubeAPI:
    def __init__(self, limit=1, query='walking'):
        self.query = query
        self.limit = limit

    def get_video_url_from_city(self, city_name, country_name):
        search_query = f"{self.query} {city_name} {country_name}"
        response = VideosSearch(search_query, limit=self.limit)
        results = response.result()['result']
        video_url = None if not results else results[0]['link']
        return video_url
    

if __name__ == "__main__":
    yt_api = YoutubeAPI()
    video_url = yt_api.get_video_url_from_city("Paris", "France")
    print(video_url)
