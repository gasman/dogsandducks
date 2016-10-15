import json
import urllib.parse
import urllib.request

from dateutil.parser import parse as parse_date

from django.core.management.base import BaseCommand, CommandError

from mapping.models import Determinand, Measurement, Sample, SamplingPoint


class Command(BaseCommand):
    help = "Import phosphate measurements from Environment Agency data"

    def handle(self, *args, **options):
        RESULT_COUNT = 1000
        BASE_URL = "http://environment.data.gov.uk/water-quality/data/measurement.json?"
        offset = 0

        # determinand = Determinand.objects.get(notation='0192')  # Phosphate
        determinand = Determinand.objects.get(notation='0180')  # Orthophosphate

        # Load all sampling points
        sampling_points_by_id_url = {
            sampling_point.id_url: sampling_point
            for sampling_point in SamplingPoint.objects.all()
        }

        samples_by_id_url = {
            sample.id_url: sample
            for sample in Sample.objects.all()
        }

        while True:
            url_params = {
                'area': '10-37',
                'determinand': determinand.notation,
                'sampledMaterialType': '2AZZ',  # RIVER / RUNNING SURFACE WATER
                '_sort': '@id',
                '_limit': RESULT_COUNT,
                '_offset': offset
            }

            data_url = BASE_URL + urllib.parse.urlencode(url_params)
            print("Fetching measurements: %d" % offset)

            with urllib.request.urlopen(data_url) as response:
                print("Importing measurements: %d" % offset)
                data = json.loads(response.read().decode('utf-8'))
                for measurement in data['items']:

                    sample_url = measurement['sample']['@id']
                    # is this a sample we already know about?
                    try:
                        sample = samples_by_id_url[sample_url]
                    except KeyError:

                        sampling_point_url = measurement['sample']['samplingPoint']['@id']
                        try:
                            sampling_point = sampling_points_by_id_url[sampling_point_url]
                        except KeyError:
                            sampling_point_label = measurement['sample']['samplingPoint']['label']
                            print("unknown sampling point %s (%s) - skipping" % (sampling_point_url, sampling_point_label))
                            continue

                        sample, _ = Sample.objects.get_or_create(id_url=sample_url, defaults={
                            'sampling_point': sampling_point,
                            'date_time': parse_date(measurement['sample']['sampleDateTime']),
                        })
                        samples_by_id_url[sample_url] = sample

                    Measurement.objects.get_or_create(id_url=measurement['@id'], defaults={
                        'sample': sample,
                        'determinand': determinand,
                        'result': measurement['result'],
                    })

            if len(data['items']) < RESULT_COUNT:
                break
            else:
                offset += RESULT_COUNT
