from django.db import models
from django.core.validators import MinValueValidator
from nt_pizza_django.models import CustomModel
from django.contrib.auth import get_user_model
from stores.models import Pizza

AuthUserModel = get_user_model()


class Order(CustomModel):
    user = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
    items = models.ManyToManyField(Pizza, through='OrderItem', related_name='orders')  # order.items / pizza.orders


class OrderItem(CustomModel):
    item = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name='order_items')  # pizza.order_items
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')  # order.order_items
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])



