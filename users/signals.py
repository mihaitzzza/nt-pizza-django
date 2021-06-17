from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import reverse
from users.models import Profile, Activation, Notification
from users.emails import send_activation_email
from utils.cart import Cart
from stores.models import Store, Pizza

AuthUserModel = get_user_model()


@receiver(post_save, sender=AuthUserModel)
def create_profile(instance, created, **kwargs):
    if created:
        Profile(user=instance).save()


@receiver(pre_save, sender=AuthUserModel)
def inactivate_user(instance, **kwargs):
    is_social_user = hasattr(instance, 'is_social_auth') and instance.is_social_auth is True
    if not instance.pk and not is_social_user:
        instance.is_active = False
        instance.password = None


@receiver(post_save, sender=AuthUserModel)
def set_activation_details(instance, created, **kwargs):
    if created:
        activation = Activation(user=instance)
        activation.save()

        send_activation_email(activation)


@receiver(user_logged_in)
def get_cart_data(request, user, **kwargs):
    Cart.load(user, request.session)


@receiver(post_save, sender=Store)
def create_store_notification(instance, created, **kwargs):
    if created:
        # users = AuthUserModel.objects.filter(is_staff=False).all()
        users = AuthUserModel.objects.exclude(is_staff=True).all()
        for user in users:
            Notification(
                user=user,
                content_object=instance,
                message='New store was added.',
                link=reverse('stores:details', args=(instance.id,)),
            ).save()


@receiver(pre_save, sender=Pizza)
def create_pizza_notification(instance, **kwargs):
    if instance.pk:  # object was already saved at a previous time.
        current_price = Pizza.objects.get(pk=instance.pk).price
        if instance.price < current_price:
            users = AuthUserModel.objects.exclude(is_staff=True).all()
            for user in users:
                Notification(
                    user=user,
                    content_object=instance,
                    message='Pizza price have dropped!',
                    link=reverse('stores:pizza:details', args=(instance.id,)),
                ).save()
