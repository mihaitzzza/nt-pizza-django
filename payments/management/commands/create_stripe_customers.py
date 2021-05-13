import stripe
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from payments.models import StripeCustomer

AuthUserModel = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = AuthUserModel.objects.filter(is_superuser=False, is_staff=False, stripe_customer__isnull=True)

        for user in users:
            stripe_customer = stripe.Customer.create(
                email=user.email,
                name='%s %s' % (user.first_name, user.last_name),
                api_key=settings.STRIPE_SECRET_KEY
            )

            print('user.email', user.email)

            StripeCustomer(user=user, stripe_id=stripe_customer['id']).save()
