import json
import urllib.request

from django.core.management.base import BaseCommand, CommandError

from mapping.models import SamplingPoint


class Command(BaseCommand):
    help = "Import sampling points from Environment Agency data"

    def handle(self, *args, **options):
        data_url = "http://environment.data.gov.uk/water-quality/id/sampling-point.json?area=10-37"

        with urllib.request.urlopen(data_url) as response:
            data = json.loads(response.read().decode('utf-8'))
            for sampling_point in data['items']:
                SamplingPoint.objects.create(
                    label=sampling_point['label'],
                    lat=sampling_point['lat'],
                    lng=sampling_point['long'],
                )
