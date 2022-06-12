from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from config.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('cars/', include("cars.urls")),
    path('api/v1/pre_order/', include('pre_order.urls')),
    path('api/v1/orders/', include('orders.urls')),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) if settings.DEBUG else urlpatterns