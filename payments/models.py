from django.db import models
from django.contrib.auth import get_user_model

AuthUserModel = get_user_model()


class StripeCustomer(models.Model):
    user = models.OneToOneField(AuthUserModel, related_name='stripe_customer', on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255, unique=True)


class StripeCard(models.Model):
    stripe_customer = models.ForeignKey(StripeCustomer, related_name='cards', on_delete=models.CASCADE)
    stripe_card_id = models.CharField(max_length=255, unique=True)
