import stripe
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from payments.models import StripeCustomer

AuthUserModel = get_user_model()


@receiver(post_save, sender=AuthUserModel)
def create_stripe_customer(instance, created, **kwargs):
    if created:
        stripe_customer = stripe.Customer.create(
            email=instance.email,
            name='%s %s' % (instance.first_name, instance.last_name),
            api_key=settings.STRIPE_SECRET_KEY
        )

        StripeCustomer(user=instance, stripe_id=stripe_customer['id']).save()
