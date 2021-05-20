from django.urls import path
from orders.views import order_view, pay_order

app_name = 'orders'

urlpatterns = [
    path('', order_view, name='order'),
    path('pay/', pay_order, name='pay'),
]