from django.test import TestCase, Client
from django.shortcuts import reverse
from django.contrib.auth import get_user, get_user_model

AuthUserModel = get_user_model()

# client = Client()
# response = client.get('http://localhost:8000/stores/pizza/?search_term=Formaggi&order_by=popularity&ingredients=230')
# response = client.get(reverse('stores:pizza:filter', kwargs={'search_term': 'Formaggi', 'order_by': 'popularity', 'ingredients': [230]}))


class AuthenticationTestCase(TestCase):
    def test_authentication_failed(self):
        login_url = reverse('users:account:login')
        client = Client()
        response = client.post(login_url, {
            'username': 'a@test.com',
            'password': '123',
        })

        # Get authenticated user (AnonymousUser if user not authenticated).
        request_user = get_user(client)

        self.assertFalse(request_user.is_authenticated)
        self.assertContains(response, "<p>Your username and password didn't match. Please try again.</p>")

    def test_authentication_succeed(self):
        user = AuthUserModel.objects.create(
            first_name='A',
            last_name='B',
            email='a@test.com',
        )
        user.is_active = True
        user.set_password('python123')
        user.save()

        client = Client()
        client.login(username='a@test.com', password='python123')
        request_user = get_user(client)

        self.assertTrue(request_user.is_authenticated)
        self.assertEqual(request_user.email, user.email)
