from locust import HttpUser, task, between, tag

class WordpressUser(HttpUser):
    wait_time = between(1, 2)

    @tag("pequena")
    @task
    def pagina_pequena(self):
        self.client.get("/2026/04/22/vaco/")