from django.db import models

from . import donor, marathon


class Donation(models.Model):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    ERROR = "ERROR"

    TRANSACTION_STATE_CHOICES = (
        (PENDING, "Pending"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
        (ERROR, "Error"),
    )

    donor = models.ForeignKey(donor.Donor, on_delete=models.PROTECT, null=True)
    event = models.ForeignKey(marathon.Marathon, on_delete=models.PROTECT)
    transaction_state = models.CharField(
        max_length=50, choices=TRANSACTION_STATE_CHOICES, default=PENDING
    )

    amount = models.DecimalField(decimal_places=2, max_digits=20)

    is_anon = models.BooleanField(default=False)

    txn_id = models.CharField(max_length=50, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} ({self.transaction_state})"
