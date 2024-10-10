from django.urls import path
from . import views
from .services import ScheduleManager

urlpatterns = [
    path('todos/', views.TodosList.as_view(), name="create-todo"),
    path('todos/delete/<str:title>/<str:item_type>', views.TodosList.as_view(), name='delete-todo'),
    path('todos/edit/<str:title>/<str:item_type>', views.TodosList.as_view(), name='edit-todo'),
    path('all/status/<str:title>/<str:item_type>', views.AllStatusChange.as_view(), name="change-status"),
    path('week/list/', views.WeekList.as_view(), name="week-list"),
    path('today/list/', views.TodayList.as_view(), name="today-list"),
    path('tasks/delete/<str:title>/<str:item_type>', ScheduleManager.delete, name="delete-task")
]