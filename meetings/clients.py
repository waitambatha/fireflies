import requests
from decouple import config
class FirefliesClient:
    BASE_URL = config('FIREFLIES_BASE_URL')
    API_KEY = config('FIREFLIES_API_KEY')

    def get_transcripts(self):
        headers = {
            'Authorization': f'Bearer {self.API_KEY}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f'{self.BASE_URL}/transcripts', headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
