import loguru
from django.test import TestCase, Client
from .models import Labels
from task_manager.users.models import Users
from django.urls import reverse


class CrudLabelsTestCase(TestCase):

    fixtures = [
        'users.json',
        'tasks.json',
        'statuses.json',
        'labels.json',
    ]

    def setUp(self):
        self.client = Client()
        self.login = reverse('login')
        self.labels = reverse('labels')
        self.labels_count_before_test = 3
        self.success_code = 200
        self.user = Users.objects.get(pk=2)
        self.data_for_form = {
            'name': 'test_label',
        }

    def test_display_labels_if_no_auth(self):
        request = self.client.get(self.labels)
        self.assertRedirects(request, self.login)

    def test_create_label_if_no_auth(self):
        url = reverse('create_label')
        request = self.client.post(url)
        self.assertRedirects(request, self.login)
        self.assertTrue(
            len(Labels.objects.all()) == self.labels_count_before_test
        )

    def test_update_label_if_no_auth(self):
        url = reverse('update_label', args=[2])
        request = self.client.post(url, self.data_for_form)
        self.assertRedirects(request, self.login)
        self.assertTrue(
            Labels.objects.get(pk=2).name == 'new label 2'
        )

    def test_delete_if_no_auth(self):
        url = reverse('delete_label', args=[11])
        request = self.client.post(url)
        self.assertRedirects(request, self.login)
        self.assertTrue(
            len(Labels.objects.all()) == self.labels_count_before_test
        )

    def test_create_label(self):
        url = reverse('create_label')
        self.client.force_login(self.user)
        request = self.client.post(url, self.data_for_form)
        loguru.logger.info(Labels.objects.get(name='test_label').id)
        self.assertRedirects(request, self.labels)
        self.assertTrue(len(Labels.objects.all()) == 4)

    def test_update_label(self):
        url = reverse('update_label', args=[11])
        self.client.force_login(self.user)
        request = self.client.post(url, self.data_for_form)
        self.assertRedirects(request, self.labels)
        self.assertTrue(
            Labels.objects.get(pk=11).name == self.data_for_form.get('name')
        )

    def test_delete_label(self):
        self.client.force_login(self.user)
        self.client.post('/labels/create/', self.data_for_form)
        self.assertEqual(len(Labels.objects.all()), 4)
        new_label_id = \
            Labels.objects.get(name=self.data_for_form.get('name')).id
        url = reverse('delete_label', args=[new_label_id])
        delete_label_resp = self.client.post(url)
        self.assertRedirects(delete_label_resp, self.labels)
        self.assertTrue(
            len(Labels.objects.all()) == self.labels_count_before_test
        )

    def test_delete_label_associated_with_task(self):
        url = reverse('delete_label', args=[11])
        self.client.force_login(self.user)
        delete_label_resp = self.client.post(url)
        self.assertRedirects(delete_label_resp, self.labels)
        self.assertTrue(
            len(Labels.objects.all()) == self.labels_count_before_test
        )
