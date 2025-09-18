from urllib.parse import urlparse
import requests


class MattermostClient:
    def __init__(self, url: str):
        self.url = urlparse(url)
        self.api_base = f"{url}/api/v4"
        self.session = requests.Session()

    def log_in_with_credentials(self, username: str, password: str):
        response = self.session.post(
            f"{self.api_base}/users/login",
            json={"login_id": username, "password": password},
        )
        response.raise_for_status()
        token = response.headers["Token"]
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        return response.json()

    def log_in_with_token(self, token: str):
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        response = self.session.get(f"{self.api_base}/users/me")
        response.raise_for_status()
        return response.json()

    def get_total_users(self):
        response = self.session.get(f"{self.api_base}/users/stats")
        response.raise_for_status()
        stats = response.json()
        return int(stats["total_users_count"])
