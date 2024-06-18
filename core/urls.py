from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('task_manager.urls', namespace='main')),
    path('users/', include('users.urls', namespace='users')),
    path('statuses/', include('statuses.urls', namespace='statuses')),
    path('tasks/', include('tasks.urls', namespace='tasks')),
    path('labels/', include('labels.urls', namespace='labels')),
]
