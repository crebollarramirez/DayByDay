from django.urls import path
from .views import create_task, list_tasks, delete_task

urlpatterns = [
    path('todos/', create_task, name="task-list"),
    path("todos/list/", list_tasks, name="list-tasks"),
    path('todos/<str:content>/', delete_task, name='delete-task'),
]