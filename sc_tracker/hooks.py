from paypal.standard.ipn.models import PayPalIPN


def handle_valid_ipn(sender: PayPalIPN, **kwargs):
    print(f"{sender=}")
