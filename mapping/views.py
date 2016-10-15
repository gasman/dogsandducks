from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from mapping.models import Photo, SamplingPoint, Determinand, Measurement


def index(request, season):
    return render(request, 'index.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'season': season,
    })


def sampling_points(request):
    data = {
        'items': [
            {
                'lat': sampling_point.lat, 'lng': sampling_point.lng, 'label': sampling_point.label
            }
            for sampling_point in SamplingPoint.objects.all()
        ]
    }
    return JsonResponse(data)


def measurements(request, determinand, season):
    determinand = get_object_or_404(Determinand, notation=determinand)

    if season == 'summer':
        measurements = Measurement.objects.filter(
            determinand=determinand,
            sample__date_time__gt='2013-03-01', sample__date_time__lt='2013-09-01'  # summer
        ).select_related('sample', 'sample__sampling_point')
    elif season == 'all':
        measurements = Measurement.objects.filter(
            sample__date_time__gt='2013-03-01', sample__date_time__lt='2013-09-01'  # summer
        ).select_related('sample', 'sample__sampling_point')
    else:
        measurements = Measurement.objects.filter(
            determinand=determinand,
            sample__date_time__gt='2013-09-01', sample__date_time__lt='2014-03-01'  # winter
        ).select_related('sample', 'sample__sampling_point')

    data = {
        'items': [
            {
                'lat': m.sample.sampling_point.lat,
                'lng': m.sample.sampling_point.lng,
                'label': m.sample.sampling_point.label,
                'date_time': m.sample.date_time,
                'result': m.result,
            }
            for m in measurements
        ]
    }
    return JsonResponse(data)


def photos(request, season):
    if season == 'summer':
        photos = Photo.objects.filter(
            date_time__gt='2013-03-01', date_time__lt='2013-09-01'  # summer
        )
    elif season == 'all':
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(
            date_time__gt='2013-09-01', date_time__lt='2014-03-01'  # winter
        )
    data = {
        'items': [
            {
                'lat': photo.lat, 'lng': photo.lng, 'image_url': photo.image_url
            }
            for photo in photos
        ]
    }
    return JsonResponse(data)
