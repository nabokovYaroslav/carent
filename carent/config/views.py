from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from cars.models import Car
from services.models import Service
from conditions.models import Condition
from utils.srcset import get_srcset, get_adaptive_image


@ensure_csrf_cookie
def index(request):
    cars = Car.objects.select_related("brand")
    conditions = Condition.objects.all()
    services = Service.objects.all()
    for car in cars:
        car.image.srcset = get_srcset(car.image.url, request.META.get('extension_image', None))
        car.image.adaptive = get_adaptive_image(car.image.url, request.META.get('extension_image', None))
        car.characteristics = {obj.attribute.name: obj.value for obj in car.eav.get_values()}
    return render(request, 'index.html', context={'cars': cars, 'conditions': conditions, 'services': services})