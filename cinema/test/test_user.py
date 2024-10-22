from django.test import TestCase

from django.core.urlresolvers import reverse
from tastypie.test import ResourceTestCaseMixin
from django.contrib.auth.models import User
from cinema.models import Profile


class UserResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(UserResourceTest, self).setUp()
        self.api_url = reverse('api_dispatch_list', kwargs={'resource_name': 'user', 'api_name': 'v1'})
        self.user_data = {
            "username": "johndoe",
            "password": "securepassword",
            "email": "johndoe@example.com",
            "birth_date": "1990-05-15",
            "bio": "A software engineer."
        }

    def test_create_user_with_profile(self):
        response = self.api_client.post(self.api_url, data=self.user_data)
        self.assertHttpCreated(response) 

        user = User.objects.get(username='johndoe')
        self.assertEqual(user.email, 'johndoe@example.com')

        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.birth_date.strftime('%Y-%m-%d'), '1990-05-15')
        self.assertEqual(profile.bio, 'A software engineer.')

    def test_create_user_without_profile(self):
        user_data = {
            "username": "janedoe",
            "password": "securepassword",
            "email": "janedoe@example.com"
        }

        response = self.api_client.post(self.api_url, data=user_data)
        self.assertHttpCreated(response)

        user = User.objects.get(username='janedoe')
        self.assertEqual(user.email, 'janedoe@example.com')

        profile = Profile.objects.get(user=user)
        self.assertIsNone(profile.birth_date)
        self.assertEqual(profile.bio, '')

    def test_invalid_user_creation(self):
        invalid_user_data = {
            "username": "janedoe",
            "password": "securepassword",
        }

        response = self.api_client.post(self.api_url, data=invalid_user_data)
        self.assertHttpBadRequest(response)
