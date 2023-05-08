from loguru import logger
from django.test import TestCase
from django.test import Client
from .models import Users
from django.urls import reverse


class CrudUsersTestCase(TestCase):
    fixtures = [
        'users.json',
        'tasks.json',
        'statuses.json',
        'labels.json',
    ]

    def setUp(self):
        self.client = Client()
        self.login = reverse('login')
        self.users = reverse('users')
        self.users_count_before_test = 6
        self.success_code = 200
        self.user1 = Users.objects.get(pk=1)
        self.user3 = Users.objects.get(pk=3)
        self.user18 = Users.objects.get(pk=18)
        self.data_for_form = {'username': 'Aleks',
                              'first_name': 'name',
                              'last_name': 'lastname',
                              'password1': 'SecretPass112',
                              'password2': 'SecretPass112',
                              }

    def test_login_page(self):
        request_to_login = self.client.get(self.login)
        self.assertEqual(request_to_login.status_code, 200)

    def test_create_user(self):
        register = reverse('create_user')
        post_request = self.client.post(register, self.data_for_form,
                                        follow=True)
        # loguru.logger.info(request.context)
        self.assertEqual(post_request.status_code, self.success_code)
        self.assertRedirects(post_request, self.login)
        self.assertEqual(len(Users.objects.all()), 7)

    def test_update_user_if_not_logged_in(self):
        response = self.client.get('/users/2/update/')
        self.assertRedirects(response, self.login)

    def test_update_user_if_logged_on_and_have_perm(self):
        url_path = reverse('update_user', args=[3])
        self.client.force_login(self.user3)
        response = self.client.get(url_path, follow=True)
        self.assertEqual(str(response.context['user'].username), 'seeu359')
        self.assertEqual(response.status_code, self.success_code)
        post_request = self.client.post(url_path, self.data_for_form)
        self.assertRedirects(post_request, self.users)
        self.assertTrue(Users.objects.get(pk=3).username == 'Aleks')

    def test_update_not_myself_user(self):
        url_path = reverse('update_user', args=[2])
        self.client.force_login(self.user3)
        response = self.client.get(url_path, follow=True)
        self.assertRedirects(response, self.users)

    def test_delete_user_if_not_logged_in(self):
        url_path = reverse('delete_user', args=[3])
        response = self.client.get(url_path)
        self.assertRedirects(response, self.login)

    def test_delete_user_if_logged_in(self):
        url_path = reverse('delete_user', args=[18])
        self.client.force_login(self.user18)
        post_request = self.client.post(url_path, follow=True)
        self.assertRedirects(post_request, self.users)
        self.assertTrue(len(Users.objects.all()) == 5)

    def test_delete_user_if_logged_on_and_have_no_perm(self):
        url_path = reverse('delete_user', args=[3])
        self.client.force_login(self.user18)
        post_request = self.client.post(url_path, follow=True)
        self.assertRedirects(post_request, self.users)
        self.assertTrue(
            len(Users.objects.all()) == self.users_count_before_test)

    def test_delete_user_associated_with_task(self):
        url_path = reverse('delete_user', args=[3])
        self.client.force_login(self.user3)
        post_request = self.client.post(url_path, follow=True)
        self.assertRedirects(post_request, self.users)
        logger.info(len(Users.objects.all()))
        self.assertTrue(len(
            Users.objects.all()) == self.users_count_before_test)
