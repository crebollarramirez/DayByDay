from django.urls import path
from . import views
from .services import ScheduleManager

urlpatterns = [
    path('todos/', views.TodosList.as_view(), name="todos"),
    path('todos/delete/<str:item_id>/<str:item_type>', views.TodosList.as_view(), name='delete-todo'),
    path('todos/edit/<str:item_id>/<str:item_type>', views.TodosList.as_view(), name='edit-todo'),
    path('all/status/<str:item_id>/<str:item_type>', views.AllStatusChange.as_view(), name="change-status"),
    path('week/list/<str:date>', views.WeekList.as_view(), name="week-list"),
    path('today/list/<str:todayDate>', views.TodayList.as_view(), name="today-list"),
    path('tasks/', views.WeekList.as_view(), name="create-task"),
    path('tasks/delete/<str:item_id>/<str:item_type>', views.WeekList.as_view(), name="delete-task"),
]