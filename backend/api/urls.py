from django.urls import path
from . import views
from .services import ScheduleManager

urlpatterns = [
    path('todos/', views.TodosList.as_view(), name="create-todo"),
    path('todos/delete/<str:title>/<str:item_type>', ScheduleManager.delete, name='delete-todo'),
    path('todos/edit/<str:title>/<str:item_type>', ScheduleManager.update, name='edit-todo'),
    path('week/list/', ScheduleManager.getWeek, name="week-list"),
    path('today/list/', ScheduleManager.getToday, name="today-list"),
    path('all/status/<str:title>/<str:item_type>', ScheduleManager.changeStatus, name="change-status"),
    path('tasks/delete/<str:title>/<str:item_type>', ScheduleManager.delete, name="delete-task")
]