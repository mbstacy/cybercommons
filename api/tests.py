__author__ = "Tyler Pearson <tdpearson>"
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory
from rest_framework import status

from api.views import APIRoot, UserProfile


class CCAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testuserpass'
        )
        self.apiroot_view = APIRoot.as_view()
        self.userprofile_view = UserProfile.as_view()

        self.factory = APIRequestFactory()
    
    def test_api_root(self):
        api_sections = {
            'Queue': {
                'Tasks': 'http://testserver/api/queue/',
                'Tasks History': 'http://testserver/api/queue/usertasks/'
            },
            'Catalog': {
                'Data Source': 'http://testserver/api/catalog/data/'
            },
            'Data Store': {
                'Mongo': 'http://testserver/api/data_store/data/'
            },
            'User Profile': {
                'User': 'http://testserver/api/user/'
            }
        }

        request = self.factory.get('/')
        force_authenticate(request, user=self.user)
        response = self.apiroot_view(request)
        # Confirm the response matches the above api_sections
        self.assertEqual(response.data, api_sections)

    def test_user_pofile_logged_in(self):
        request = self.factory.get('/user')
        force_authenticate(request, user=self.user)
        response = self.userprofile_view(request)
        # Confirm the username exists and matches our test user
        self.assertEqual(response.data.get('username'), self.user.username)
        # Confirm that the test user has an auth-token
        self.assertTrue(response.data.get('authentication', {}).get('auth-token'))

    def test_user_profile_not_logged_in(self):
        request = self.factory.get('/user')
        response = self.userprofile_view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

