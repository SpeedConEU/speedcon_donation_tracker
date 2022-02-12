import decimal

from django.db import models


class Marathon(models.Model):
    DONATION_MINIMUM_DEFAULT = decimal.Decimal(1.0)
    EURO = "EUR"
    USD = "USD"
    SEK = "SEK"
    CURRENCY_CHOICES = [(EURO, "Euro"), (USD, "U.S. Dollar"), (SEK, "Swedish Krona")]

    start_time = models.DateTimeField()
    name = models.CharField(max_length=100, help_text="Name of the Marathon")
    slug = models.SlugField(max_length=20, unique=True, allow_unicode=False)
    recipient_name = models.CharField(
        max_length=100, blank=True, verbose_name="Donation Recipient"
    )
    recipient_paypal = models.EmailField()
    donation_minimum = models.DecimalField(
        max_digits=10, decimal_places=2, default=DONATION_MINIMUM_DEFAULT
    )
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=EURO)
    accept_donations = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_latest_marathon():
        marathon = Marathon.objects.order_by("-start_time")
        return marathon[0] if len(marathon) != 0 else None

    # returns the donation total as a simple decimal number
    def donations_get_total(self):
        from .donation import Donation

        # FIXME: this can probably be done better
        return sum(
            donation.amount
            for donation in self.donation_set.filter(
                transaction_state=Donation.COMPLETED
            )
        )

    def __str__(self):
        return self.name
