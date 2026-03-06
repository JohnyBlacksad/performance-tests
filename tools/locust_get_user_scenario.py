from locust import HttpUser, between, task
from tools.fakers import faker_ru

class GetUserScenarioUser(HttpUser):
    wait_time = between(1, 3)
    user_data: dict

    def on_start(self) -> None:
        request = {
            "email": faker_ru.email(),
            "lastName": faker_ru.last_name(),
            "firstName": faker_ru.first_name(),
            "middleName": faker_ru.middle_name(),
            "phoneNumber": faker_ru.phone_number()
        }
        response = self.client.post("/api/v1/users", json=request)
        self.user_data = response.json()

    @task
    def get_user(self):
        self.client.get(f'/api/v1/users/{self.user_data.get('user').get('id')}', name='/api/v1/users/{user_id}') # type: ignore