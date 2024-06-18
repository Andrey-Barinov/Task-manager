from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('task_manager.task_manager_main.urls', namespace='main')),
    path('users/', include('task_manager.users.urls', namespace='users')),
    path('statuses/',
         include('task_manager.statuses.urls', namespace='statuses')),
    path('tasks/', include('task_manager.tasks.urls', namespace='tasks')),
    path('labels/', include('task_manager.labels.urls', namespace='labels')),
]
