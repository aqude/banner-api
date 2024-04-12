from locust import HttpUser, task, between
import json
import random


class UserBehavior(HttpUser):
    wait_time = between(1, 2.5)

    @task(10)
    def create_banner(self):
        self.headers = {'accept': "application/json", 'token': "admin_token"}
        self.data = {
            "tag_ids": [10, 11],
            "feature_id": random.randint(0, 1000),
            "content": {
                "title": str(random.randint(0, 1000)),
                "text": str(random.randint(0, 1000)),
                "url": "https://google.com",
            },
            "is_active": True
        }

        self.client.post("/banner", data=json.dumps(self.data), headers=self.headers)
