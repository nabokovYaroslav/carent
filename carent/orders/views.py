import json

from django.http import HttpResponse
from cars.models import Car

from orders.forms import OrderForm


def create_order(request):
    data = json.loads(request.body)
    name = data.get("name", None)
    phone = data.get("phone", None)
    day = data.get("day", None)
    car_id = data.get("car_id", None)
    cost = Car.objects.only("id").get(id=car_id).price_with_discount * day
    orderform = OrderForm(data={'name': name, 'phone': phone, 'car': car_id, 'day': day, 'cost': cost})
    if orderform.is_valid():
        orderform.save()
    else:
        return HttpResponse(json.dumps({'error': 'Неправильные данные','fields':orderform.errors.as_json()}), content_type="application/json", status=400)
    return HttpResponse(status=201)