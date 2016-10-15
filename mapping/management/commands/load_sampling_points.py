import json
import urllib.parse
import urllib.request

from django.core.management.base import BaseCommand, CommandError

from mapping.models import SamplingPoint


class Command(BaseCommand):
    help = "Import sampling points from Environment Agency data"

    def handle(self, *args, **options):
        RESULT_COUNT = 1000
        BASE_URL = "http://environment.data.gov.uk/water-quality/id/sampling-point.json?"
        offset = 0

        while True:
            url_params = {
                'area': '10-37',
                '_sort': '@id',
                '_limit': RESULT_COUNT,
                '_offset': offset
            }

            data_url = BASE_URL + urllib.parse.urlencode(url_params)
            print("Fetching sampling points: %d" % offset)

            with urllib.request.urlopen(data_url) as response:
                data = json.loads(response.read().decode('utf-8'))
                for sampling_point in data['items']:
                    SamplingPoint.objects.get_or_create(id_url=sampling_point['@id'], defaults={
                        'label': sampling_point['label'],
                        'lat': sampling_point['lat'],
                        'lng': sampling_point['long'],
                    })

            if len(data['items']) < RESULT_COUNT:
                break
            else:
                offset += RESULT_COUNT
