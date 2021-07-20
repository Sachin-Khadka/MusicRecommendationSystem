from django.apps import AppConfig


class MyAccountConfig(AppConfig):
    name = 'my_account'

    def ready(self):
        import my_account.signals