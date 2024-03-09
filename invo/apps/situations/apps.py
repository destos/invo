from django.apps import AppConfig


class SituationsAppConfig(AppConfig):
    name = "situations"

    def ready(self) -> None:
        Situation = self.get_model("Situation")
        super().ready()
