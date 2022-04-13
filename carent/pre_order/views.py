import json

from django.http import HttpResponse

from pre_order.forms import PreOrderForm


def create_pre_order(request):
    data = json.loads(request.body)
    name = data.get("name", None)
    phone = data.get("phone", None)
    car_id = data.get("car_id", None)
    pre_orderform = PreOrderForm(data={'name': name, 'phone': phone, 'car': car_id})
    if pre_orderform.is_valid():
        pre_orderform.save()
    else:
        return HttpResponse(json.dumps({'error': 'Неправильные данные','fields':pre_orderform.errors.as_json()}), content_type="application/json", status=400)
    return HttpResponse(status=201)