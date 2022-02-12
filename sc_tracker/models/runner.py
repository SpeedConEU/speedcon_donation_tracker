from django.db import models


class Runner(models.Model):
    display_name = models.CharField(max_length=50)
    twitter_name = models.CharField(
        max_length=50, help_text="should be prefixed with an @"
    )
    twitch_name = models.CharField(max_length=50, blank=True)
    youtube_name = models.CharField(max_length=50, blank=True)
    country_code = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return self.display_name
