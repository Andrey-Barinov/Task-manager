from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView
)
from task_manager.mixins import UserLoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CreateTaskFrom, UpdateTaskForm
from django.urls import reverse_lazy
from .mixins import AuthorPermissionTestMixin
from .models import Task
from django.utils.translation import gettext_lazy as _


class TasksView(UserLoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks.html'
    context_object_name = 'tasks'


class TaskDetailView(UserLoginRequiredMixin, DetailView):
    model = Task
    template_name = 'detail_task.html'
    context_object_name = 'task'


class CreateTaskView(UserLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = CreateTaskFrom
    template_name = 'create_task.html'
    success_message = _('Task successfully created')
    success_url = reverse_lazy('tasks:tasks')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTaskView(UserLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = UpdateTaskForm
    template_name = 'update_task.html'
    success_message = _('Task successfully changed')
    success_url = reverse_lazy('tasks:tasks')


class DeleteTaskView(UserLoginRequiredMixin,
                     SuccessMessageMixin,
                     AuthorPermissionTestMixin,
                     DeleteView):
    model = Task
    template_name = 'delete_task.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = _('Task successfully deleted')
