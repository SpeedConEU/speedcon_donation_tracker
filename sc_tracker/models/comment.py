from django.db import models

from . import donation


class Comment(models.Model):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    READ = "READ"
    BLOCKED = "BLOCKED"

    COMMENT_STATE_CHOICES = (
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (READ, "Read"),
        (BLOCKED, "Blocked"),
    )

    id = models.OneToOneField(
        donation.Donation, on_delete=models.CASCADE, primary_key=True
    )
    text = models.TextField(blank=True, max_length=1000)
    state = models.CharField(
        choices=COMMENT_STATE_CHOICES, default=PENDING, max_length=50
    )
