from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from cars.models import Car
from utils.srcset import get_srcset, get_adaptive_image, get_tumbnail


@ensure_csrf_cookie
def car_detail(request, pk=None):
    car = Car.objects.select_related("brand").prefetch_related("carimage_set").get(pk=pk)
    car.image.srcset = get_srcset(car.image.url, request.META.get('extension_image', None))
    car.image.adaptive = get_adaptive_image(car.image.url, request.META.get('extension_image', None))
    car.image.tumbnail = get_tumbnail(car.image.url, request.META.get('extension_image', None))
    car.characteristics = {obj.attribute.name: obj.value for obj in car.eav.get_values()}
    for car_image in car.carimage_set.all():
        car_image.image.srcset = get_srcset(car_image.image.url, request.META.get('extension_image', None))
        car_image.image.adaptive = get_adaptive_image(car_image.image.url, request.META.get('extension_image', None))
        car_image.image.tumbnail = get_tumbnail(car_image.image.url, request.META.get('extension_image', None))
    cars = Car.objects.select_related("brand").exclude(pk=pk)
    for _car in cars:
        _car.image.srcset = get_srcset(_car.image.url, request.META.get('extension_image', None))
        _car.image.adaptive = get_adaptive_image(_car.image.url, request.META.get('extension_image', None))
        _car.characteristics = {obj.attribute.name: obj.value for obj in _car.eav.get_values()}
    return render(request, 'cars/car_detail.html', context={'cars': cars, 'car': car})