from django.test import TestCase, Client
from django.urls import reverse
from .models import Tasks
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels
from task_manager.users.models import Users


class CrudTasksTestCase(TestCase):

    fixtures = [
        'users.json',
        'tasks.json',
        'statuses.json',
        'labels.json',
    ]

    def setUp(self):
        self.client = Client()
        self.login = reverse('login')
        self.tasks = reverse('tasks')
        self.tasks_count_before_test = 6
        self.success_code = 200
        self.status = Statuses.objects.get(pk=8)
        self.label = Labels.objects.get(pk=2)
        self.user = Users.objects.get(pk=4)
        self.data_for_form = {
            'name': 'test_task',
            'description': 'test description',
            'status': self.status.id,
            'executor': self.user.id,
            'creator': self.user.id,
            'labels': self.label.id,
        }

    def test_display_task_if_no_auth(self):
        request = self.client.get(self.tasks)
        self.assertRedirects(request, self.login)

    def test_create_task_if_no_auth(self):
        url = reverse('create_task')
        request = self.client.post(url)
        self.assertRedirects(request, self.login)
        self.assertTrue(
            len(Tasks.objects.all()) == self.tasks_count_before_test
        )

    def test_update_task_if_no_auth(self):
        url = reverse('update_task', args=[10])
        request = self.client.post(url, self.data_for_form)
        self.assertRedirects(request, self.login)
        self.assertTrue(
            Tasks.objects.get(name='another task').name == 'another task'
        )

    def test_delete_task_if_no_auth(self):
        url = reverse('delete_task', args=[9])
        request = self.client.post(url)
        self.assertRedirects(request, self.login)
        self.assertTrue(
            len(Tasks.objects.all()) == self.tasks_count_before_test)

    def test_create_task(self):
        url = reverse('create_task')
        self.client.force_login(self.user)
        request = self.client.post(url, self.data_for_form)
        self.assertRedirects(request, self.tasks)
        self.assertTrue(
            len(Tasks.objects.all()) == 7)

    def test_update_task(self):
        url = reverse('update_task', args=[5])
        self.client.force_login(self.user)
        request = self.client.post(url, self.data_for_form)
        self.assertRedirects(request, self.tasks)
        self.assertTrue(
            Tasks.objects.get(pk=5).name == self.data_for_form.get('name')
        )

    def test_delete_task(self):
        url = reverse('delete_task', args=[5])
        self.client.force_login(self.user)
        request = self.client.post(url)
        self.assertRedirects(request, self.tasks)
        self.assertTrue(
            len(Tasks.objects.all()) == 5
        )

    def test_delete_not_self_task(self):
        url = reverse('delete_task', args=[9])
        self.client.force_login(self.user)
        request = self.client.post(url)
        self.assertRedirects(request, self.tasks)
        self.assertTrue(
            len(Tasks.objects.all()) == self.tasks_count_before_test
        )
