from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = "accounts"
    verbose_name = "Invo Accounts"

    # def ready(self):
    #     from django_q.tasks import schedule, Schedule
    #     schedule(
    #         "accounts.tasks.flush_expired_tokens_command",
    #         name="Clear tokens daily",
    #         schedule_type=Schedule.DAILY,
    #         catch_up=False
    #     )
