from django.db import models


class Donor(models.Model):
    alias = models.CharField(max_length=50)
    payer_id = models.CharField(max_length=50, blank=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.alias
