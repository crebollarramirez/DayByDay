from django.urls import path
from .views import *
from .services import ScheduleManager

urlpatterns = [
    path('todos/', ScheduleManager.create, name="create-todo"),
    path("todos/list/", ScheduleManager.getTodos, name="todo-list"),
    path('todos/delete/<str:title>/<str:item_type>', ScheduleManager.delete, name='delete-todo'),
    path('todos/edit/<str:title>/<str:item_type>', ScheduleManager.update, name='edit-todo'),
    path('week/list/', ScheduleManager.getWeek, name="week-list")
]