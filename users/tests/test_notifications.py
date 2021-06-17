from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models.user_data import Notification
from stores.models import Store, Pizza

AuthUserModel = get_user_model()


class NotificationTestCase(TestCase):
    def setUp(self) -> None:
        AuthUserModel.objects.create(
            first_name='Notified',
            last_name='User',
            email='a@test.com',
        )
        store_owner = AuthUserModel.objects.create(
            first_name='Store',
            last_name='Owner',
            email='b@test.com',
            is_staff=True,
        )
        Store.objects.create(
            owner=store_owner,
            name='Store #1',
        )

    def test_store_notification_type(self):
        # Retrieve data
        notified_user = AuthUserModel.objects.get(email='a@test.com')
        store = Store.objects.get(name='Store #1')
        notification = Notification.objects.create(
            user=notified_user,
            content_object=store,
            message='Notification #1',
            link='test_link'
        )

        # Check results
        self.assertEqual(notification.get_content_object_type().__name__, Store.__name__)

    def test_pizza_notification_type(self):
        # Data setup
        store = Store.objects.get(name='Store #1')
        Pizza.objects.create(
            store=store,
            name='Pizza #1',
        )

        # Retrieve data
        notified_user = AuthUserModel.objects.get(email='a@test.com')
        pizza = Pizza.objects.get(name='Pizza #1')
        notification = Notification.objects.create(
            user=notified_user,
            content_object=pizza,
            message='Notification #1',
            link='test_link'
        )

        # Check results
        self.assertEqual(notification.get_content_object_type().__name__, Pizza.__name__)
