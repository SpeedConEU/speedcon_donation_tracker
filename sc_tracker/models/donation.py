from django.db import models

from . import donor, marathon
from ..validator import validate_positive


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

    donor = models.ForeignKey(donor, on_delete=models.PROTECT, null=True)
    event = models.ForeignKey(marathon, on_delete=models.PROTECT)
    transaction_state = models.CharField(
        max_length=50, choices=TRANSACTION_STATE_CHOICES, default=PENDING
    )

    amount = models.DecimalField(
        decimal_places=2, max_digits=20, validators=[validate_positive]
    )
