import requests
import time

class ByteDanceClient:
    def __init__(self, api_key: str, base_url: str = "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def post(self, endpoint: str, payload: dict, retries: int = 3, backoff: int = 2):
        url = f"{self.base_url}{endpoint}"
        for attempt in range(retries):
            try:
                response = requests.post(url, json=payload, headers=self.headers, timeout=60)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                if attempt < retries - 1:
                    time.sleep(backoff * (attempt + 1))
                else:
                    raise e

