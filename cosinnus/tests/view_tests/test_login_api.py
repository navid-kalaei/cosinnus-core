import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class LoginViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.login_url = reverse('cosinnus:frontend-api:api-login')

        self.user_data = {
            'username': 'testuser@mail.io',
            'password': '12345'
        }

        self.another_user_data = {
            'username': 'another_user@mail.io',
            'password': 'some_password'
        }

        self.user = User.objects.create_user(username='testuser@mail.io', email='testuser@mail.io', password='12345', is_active=True)
        self.user.save()

        self.another_user = User.objects.create_user(username='another_user@mail.io', email='another_user@mail.io', password='some_password', is_active=True)
        self.another_user.save()

        return super().setUp()

    def test_login_successful(self):
        """
        Ensure we can login with given user data and the user gets authenticated after all
        """
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 200)
        s = self.client.session.get('_auth_user_id') # get the user's auth id
        self.assertEqual(int(s), self.user.pk) # check if user's auth id and user's pk are equal -> in case they are, user is authenticated

    def test_login_with_empty_data(self):
        """
        Ensure that the user login data cannot be empty
        """
        self.client.get('/language/en/') # set language to english so the strings can be compared
        response = self.client.post(self.login_url, {"username": "", "password": ""}, format='json')
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertIn("This field may not be blank.", response_json.get('data', {}).get('username'))
        self.assertIn("This field may not be blank.", response_json.get('data', {}).get('password'))
        s = self.client.session.get('_auth_user_id') # get the user's auth id, should be None because non authenticated
        self.assertEqual(s, None, 'user should not be logged in with no authentication')
        
    def test_login_with_incorrect_password(self):
        """
        Ensure user cannot login using incorrect password
        """
        response = self.client.post(self.login_url, {'username': self.user_data['username'], 'password': 'incorrect_passeord'}, format='json')
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertIn('Incorrect email or password', response_json.get('data', {}).get('non_field_errors'))
        s = self.client.session.get('_auth_user_id') # get the user's auth id, should be None because non authenticated
        self.assertEqual(s, None, 'user should not be logged in with an incorrect password')

    def test_login_with_false_username(self):
        """
        Ensure user cannot login using false username
        """
        response = self.client.post(self.login_url, {'username': 'false_username@mail.io', 'password': self.user_data['password']}, format='json')
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertIn('Incorrect email or password', response_json.get('data', {}).get('non_field_errors'))
        s = self.client.session.get('_auth_user_id') # get the user's auth id, should be None because non authenticated
        self.assertEqual(s, None, 'user should not be logged in with an incorrect username')
        
    def test_login_with_non_email_like_username(self):
        """
        Ensure user cannot login using false username which is not an email
        """
        self.client.get('/language/en/')
        response = self.client.post(self.login_url, {'username': 'false_username', 'password': self.user_data['password']}, format='json')
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertIn('Enter a valid email address.', response_json.get('data', {}).get('username'))
        s = self.client.session.get('_auth_user_id') # get the user's auth id, should be None because non authenticated
        self.assertEqual(s, None, 'user should not be logged in with an invalid email')

    def test_deactivated_user_cannot_login(self):
        """
        Ensure user cannot login being not active / beind deactivated
        """
        self.user.is_active = False
        self.user.save()

        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, 400)
        response_json = json.loads(response.content)
        self.assertIn('Incorrect email or password', response_json.get('data', {}).get('non_field_errors'))
        s = self.client.session.get('_auth_user_id') # get the user's auth id, should be None because non authenticated
        self.assertEqual(s, None, 'deactivated user should not be logged in')
        
    def test_another_user_cannot_login_with_first_user_logged_in(self):
        """
        Ensure that no user can login with another user being already logged in
        """
        response_user = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response_user.status_code, 200)
        response_another_user = self.client.post(self.login_url, self.another_user_data, format='json')
        self.assertEqual(response_another_user.status_code, 403, "a second log in during an active session should not be possible")
        s = self.client.session.get('_auth_user_id')
        self.assertEqual(int(s), self.user.pk, "this user should be logged in")
        self.assertNotEqual(int(s), self.another_user.pk, "this user should not be logged in")