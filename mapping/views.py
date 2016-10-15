from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from mapping.models import SamplingPoint


def index(request):
    return render(request, 'index.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
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
