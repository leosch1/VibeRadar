from requests import get, post, HTTPError
import time

class Chartmetric_api():
    def __init__(self):
        self.refresh_token = 'dId4aE8UQ7CqAejq6RLISqKakgzpWJz4bC0C4hPYxxcTYm9Me925VphIE4yIMr4H'
        self.base_url = "https://api.chartmetric.com"
        self._update_api_token()

    def _update_api_token(self):
        res = post(f'{self.base_url}/api/token', json={"refreshtoken": self.refresh_token})
        if res.status_code != 200:
            raise HTTPError(f'ERROR: received a {res.status_code}')
        self.last_token_updated = time.time()
        self.access_token = res.json()['token']

    def Get(self, uri):
        if time.time() - self.last_token_updated > 3600:
            self._update_api_token()
        return get(f'{self.base_url}{uri}', headers={'Authorization': f'Bearer {self.access_token}'})

if __name__ == '__main__':
    api = Chartmetric_api()
    api.Get('/api/city/592/youtube/top-tracks')
