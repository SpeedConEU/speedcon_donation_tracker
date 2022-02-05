from django.db import models


class Donor(models.Model):


    alias = models.CharField(max_length=50)
    is_anon = models.BooleanField()
