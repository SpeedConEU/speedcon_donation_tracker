from django.apps import AppConfig
from paypal.standard.ipn.signals import valid_ipn_received


class ScTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sc_tracker'

    def ready(self):
        from .hooks import handle_valid_ipn
        valid_ipn_received.connect(handle_valid_ipn)
