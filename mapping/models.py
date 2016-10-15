from django.db import models


class SamplingPoint(models.Model):
    label = models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.label
