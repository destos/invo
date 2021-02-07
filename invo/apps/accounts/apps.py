from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = "accounts"
    verbose_name = "Invo Accounts"

    # from django_q.tasks import schedule
    # schedule("accounts.tasks.flush_expired_tokens_command", name="", schedule_type=Schedule.DAILY, catch_up=False)
