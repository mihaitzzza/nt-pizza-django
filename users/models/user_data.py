from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from utils.constants import SHIPPING_ADDRESS, BILLING_ADDRESS
from nt_pizza_django.models import CustomModel

AuthUserModel = get_user_model()


# Create your models here.
class Address(CustomModel):
    user = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
    street = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=255, null=False)
    country = models.CharField(max_length=255, null=False)

    class Types(models.IntegerChoices):
        SHIPPING = SHIPPING_ADDRESS
        BILLING = BILLING_ADDRESS
    type = models.IntegerField(choices=Types.choices, null=False, default=SHIPPING_ADDRESS)


class Profile(CustomModel):
    user = models.OneToOneField(AuthUserModel, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profiles', default=None, null=True)


class Notification(CustomModel):
    user = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    seen = models.BooleanField(default=False)
