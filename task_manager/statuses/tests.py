from django.test import TestCase, Client
from django.urls import reverse
from .models import Statuses
from task_manager.users.models import Users


class CrudStatusesTestCases(TestCase):

    fixtures = [
        'users.json',
        'tasks.json',
        'statuses.json',
        'labels.json',
    ]

    def setUp(self):
        self.client = Client()
        self.login = reverse('login')
        self.statuses = reverse('statuses')
        self.statuses_count_before_test = 3
        self.success_code = 200
        self.user = Users.objects.get(pk=2)
        self.data_for_form = {
            'name': 'test_status',
        }

    def test_display_statuses_if_no_auth(self):
        request = self.client.get(self.statuses)
        self.assertRedirects(request, self.login)

    def test_create_status_if_no_auth(self):
        request = self.client.get('/statuses/create/')
        self.assertRedirects(request, self.login)

    def test_update_status_if_no_auth(self):
        url_path = reverse('update_status', args=[9])
        request = self.client.get(url_path)
        self.assertRedirects(request, self.login)

    def test_delete_status_if_no_auth(self):
        url_path = reverse('delete_status', args=[1])
        request = self.client.get(url_path)
        self.assertRedirects(request, self.login)

    def test_create_status(self):
        url_path = reverse('create_status')
        self.client.force_login(self.user)
        request = self.client.get(url_path)
        self.assertTrue(request.status_code == self.success_code)
        create_status_resp = self.client.post(url_path,
                                              self.data_for_form,
                                              follow=True,
                                              )
        self.assertRedirects(create_status_resp, self.statuses)
        self.assertEqual(len(Statuses.objects.all()), 4)

    def test_update_status(self):
        url_path = reverse('update_status', args=[8])
        self.client.force_login(self.user)
        request = self.client.get(url_path)
        self.assertTrue(request, self.success_code)
        update_status_resp = self.client.post(url_path,
                                              self.data_for_form,
                                              follow=True,
                                              )
        self.assertRedirects(update_status_resp, self.statuses)
        self.assertTrue(
            Statuses.objects.get(pk=8).name == self.data_for_form['name']
        )

    def test_delete_status(self):
        url_path = reverse('delete_status', args=[9])
        self.client.force_login(self.user)
        request_get = self.client.get(url_path)
        self.assertTrue(request_get.status_code == self.success_code)
        delete_status_resp = self.client.post(url_path)
        self.assertRedirects(delete_status_resp, self.statuses)
        self.assertTrue(len(Statuses.objects.all()) == 2)

    def test_delete_status_associated_with_task(self):
        url_path = reverse('delete_status', args=[8])
        self.client.force_login(self.user)
        request_get = self.client.get(url_path)
        self.assertTrue(request_get.status_code == self.success_code)
        delete_status_resp = self.client.post(url_path)
        self.assertRedirects(delete_status_resp, self.statuses)
        self.assertTrue(
            len(Statuses.objects.all()) == self.statuses_count_before_test
        )
