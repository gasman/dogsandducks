from django.db import models


class SamplingPoint(models.Model):
    id_url = models.URLField(unique=True)
    label = models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.label


class Photo(models.Model):
    image_url = models.URLField()
    lat = models.FloatField()
    lng = models.FloatField()
    date_time = models.DateTimeField(null=True)


class Sample(models.Model):
    id_url = models.URLField(unique=True)
    sampling_point = models.ForeignKey(SamplingPoint, on_delete=models.CASCADE, related_name='samples')
    date_time = models.DateTimeField()


class Determinand(models.Model):
    id_url = models.URLField(unique=True)
    label = models.CharField(max_length=255)
    notation = models.CharField(max_length=30)

    def __str__(self):
        return self.label


class Measurement(models.Model):
    id_url = models.URLField(unique=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='measurements')
    determinand = models.ForeignKey(Determinand, on_delete=models.CASCADE, related_name='+')
    result = models.FloatField()
