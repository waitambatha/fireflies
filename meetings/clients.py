import requests
from decouple import config


class FirefliesClient:
    BASE_URL = config('FIREFLIES_BASE_URL')  # Example: 'https://api.fireflies.ai/graphql'
    API_KEY = config('FIREFLIES_API_KEY')

    def get_users(self):
        url = self.BASE_URL
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.API_KEY}'
        }
        data = {
            'query': '{ users { name user_id } }'
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
