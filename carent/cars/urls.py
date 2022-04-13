from django.urls import path

from cars.views import car_detail


urlpatterns = [
    path('<int:pk>/', car_detail, name="car_detail")
]
