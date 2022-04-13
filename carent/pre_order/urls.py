from django.urls import path

from pre_order.views import create_pre_order


urlpatterns = [
    path('', create_pre_order)
]
