from locust import HttpUser, task, between, tag

PAGINA_PEQUENA = "/2026/05/13/pagina-pequena/"
PAGINA_MEDIA = "/2026/05/13/pagina-media/"
PAGINA_GRANDE = "/2026/05/13/pagina-grande/"


class WordpressUser(HttpUser):
    wait_time = between(1, 2)

    def consultar_pagina_pequena(self):
        self.client.get(PAGINA_PEQUENA, name="pagina pequena")

    def consultar_pagina_media(self):
        self.client.get(PAGINA_MEDIA, name="pagina media")

    def consultar_pagina_grande(self):
        self.client.get(PAGINA_GRANDE, name="pagina grande")

    @tag("pequena")
    @task
    def pagina_pequena(self):
        self.consultar_pagina_pequena()

    @tag("media")
    @task
    def pagina_media(self):
        self.consultar_pagina_media()

    @tag("grande")
    @task
    def pagina_grande(self):
        self.consultar_pagina_grande()

    @tag("misto")
    @task
    def paginas_pequena_media_grande(self):
        self.consultar_pagina_pequena()
        self.consultar_pagina_media()
        self.consultar_pagina_grande()
