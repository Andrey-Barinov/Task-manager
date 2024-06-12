from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.messages import get_messages
from .forms import CreateTaskFrom
from .models import Status
from tasks.models import Task
from django.contrib.auth.views import get_user_model

test_user1 = {
    "first_name": "test1_first_name",
    "last_name": "test1_last_name",
    "username": "test1_username",
    "password": "test1"
}


class TestCreateTaskView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user1)

    def test_create_task_get_with_unknown_user(self):
        response = self.client.get(reverse_lazy('tasks:create'))

        self.assertRedirects(
            response,
            reverse_lazy('login'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_create_task_get(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.get(reverse_lazy('tasks:create'))

        self.assertTemplateUsed(response, 'create_task.html')
        self.assertContains(response, 'Имя', status_code=200)
        self.assertContains(response, 'Описание', status_code=200)
        self.assertContains(response, 'Статус', status_code=200)
        self.assertContains(response, 'Исполнитель', status_code=200)

    def test_create_task_post(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        status = Status.objects.create(name='Test_status')
        author = get_user_model().objects.get(username=test_user1['username'])
        response = self.client.post(reverse_lazy('tasks:create'), {
            "name": "test_task",
            "status": status.pk
        })

        self.assertRedirects(
            response,
            reverse_lazy('tasks:tasks'),
            status_code=302,
            target_status_code=200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно создана')

        new_task = Task.objects.get(name="test_task")
        self.assertTrue(new_task)
        self.assertEqual(new_task.author, author)


class TestCreateTaskFrom(TestCase):

    def test_right(self):
        status = Status.objects.create(name='Test_status')
        form = CreateTaskFrom(data={
            "name": "test_first_name",
            "status": status
        })
        self.assertTrue(form.is_valid())

    def test_with_empty_name_field(self):
        status = Status.objects.create(name='Test_status')
        form = CreateTaskFrom(data={
            "name": "",
            "status": status
        })
        self.assertFalse(form.is_valid())

    def test_with_empty_status_field(self):
        form = CreateTaskFrom(data={
            "name": "test_first_name",
            "status": ''
        })
        self.assertFalse(form.is_valid())


class TestDeleteTaskView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user1)
        status = Status.objects.create(name='Test_status')
        author = get_user_model().objects.get(username=test_user1['username'])
        Task.objects.create(name="test_task", status=status, author=author)

    def test_delete_task_get_with_unknown_user(self):
        response = self.client.get(reverse_lazy(
            'tasks:delete', kwargs={'pk': 1})
        )

        self.assertRedirects(
            response,
            reverse_lazy('login'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_delete_task_get(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.get(reverse_lazy(
            'tasks:delete', kwargs={'pk': 1})
        )

        self.assertTemplateUsed(response, 'delete_task.html')
        self.assertContains(response,
                            'Вы уверены, что хотите удалить test_task?',
                            status_code=200)
        self.assertContains(response, 'Да, удалить', status_code=200)

    def test_delete_task_post(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.post(
            reverse_lazy('tasks:delete', kwargs={'pk': 1})
        )

        self.assertRedirects(
            response,
            reverse_lazy('tasks:tasks'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно удалена')

        self.assertFalse(Task.objects.filter(name='test_task'))


class TestUpdateTaskView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user1)
        status = Status.objects.create(name='Test_status')
        author = get_user_model().objects.get(username=test_user1['username'])
        Task.objects.create(name="test_task", status=status, author=author)

    def test_update_task_get_with_unknown_user(self):
        response = self.client.get(reverse_lazy(
            'tasks:update', kwargs={'pk': 1})
        )

        self.assertRedirects(
            response,
            reverse_lazy('login'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_update_task_get(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.get(reverse_lazy(
            'tasks:update', kwargs={'pk': 1})
        )

        self.assertTemplateUsed(response, 'update_task.html')
        self.assertContains(response, "test_task", status_code=200)

    def test_update_task_post(self):
        status = Status.objects.create(name='Test_status')
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.post(reverse_lazy('tasks:update',
            kwargs={'pk': 1}),
            {
            "name": "changed_test_task",
            "status": status.pk
        })

        self.assertRedirects(
            response,
            reverse_lazy('tasks:tasks'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно изменена')

        changed_task = Task.objects.get(name="changed_test_task")
        self.assertEqual(changed_task.name, "changed_test_task")


class TestTaskDetailView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user1)
        status = Status.objects.create(name='Test_status')
        author = get_user_model().objects.get(username=test_user1['username'])
        Task.objects.create(name="test_task", status=status, author=author)

    def test_task_detail_with_unknown_user(self):
        response = self.client.get(
            reverse_lazy('tasks:detail', kwargs={'pk': 1}))

        self.assertRedirects(
            response,
            reverse_lazy('login'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_tasks(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.get(
            reverse_lazy('tasks:detail', kwargs={'pk': 1}))

        self.assertTemplateUsed(response, 'detail_task.html')
        self.assertContains(response, "test_task", status_code=200)
        self.assertContains(response, 'Test_status', status_code=200)


class TestTasksView(TestCase):
    def setUp(self):
        users = get_user_model()
        users.objects.create_user(**test_user1)
        status = Status.objects.create(name='Test_status')
        author = get_user_model().objects.get(username=test_user1['username'])
        Task.objects.create(name="test_task1", status=status, author=author)
        Task.objects.create(name="test_task2", status=status, author=author)

    def test_tasks_with_unknown_user(self):
        response = self.client.get(reverse_lazy('tasks:tasks'))

        self.assertRedirects(
            response,
            reverse_lazy('login'),
            status_code=302,
            target_status_code=200)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         'Вы не авторизованы! Пожалуйста, выполните вход.')

    def test_tasks(self):
        self.client.login(
            username=test_user1['username'],
            password=test_user1['password'])
        response = self.client.get(reverse_lazy('tasks:tasks'))

        self.assertTemplateUsed(response, 'tasks.html')
        self.assertContains(response, "test_task1", status_code=200)
        self.assertContains(response, "test_task2", status_code=200)
