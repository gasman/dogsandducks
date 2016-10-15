import csv
import datetime

from django.core.management.base import BaseCommand, CommandError

from mapping.models import Photo


class Command(BaseCommand):
    help = "Import Flickr photos from CSV"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):
        with open(options['filename']) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                timestamp = int(float(row['1305891095']))
                if timestamp > 0:
                    t = datetime.datetime.fromtimestamp(timestamp)
                else:
                    t = None

                Photo.objects.get_or_create(
                    lat=row['Unnamed__1'],
                    lng=row['Unnamed_ 1'],
                    image_url=row['http_//far'],
                    date_time=t
                )
