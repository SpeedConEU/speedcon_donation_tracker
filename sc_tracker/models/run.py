import datetime

from django.db import models

from . import Marathon, Runner


class Run(models.Model):
    marathon = models.ForeignKey(Marathon, on_delete=models.PROTECT)
    runners = models.ManyToManyField(Runner)

    game_name = models.CharField(max_length=70)
    category = models.CharField(max_length=50)
    platform = models.CharField(max_length=50, blank=True)
    estimate = models.DurationField()
    additional_setup = models.DurationField(
        default=datetime.timedelta(),
        help_text="will be added on top of the estimate when calculating the next run start",
    )

    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.game_name} ({self.category}"

    class Meta(object):
        ordering = ["order"]
