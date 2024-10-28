from django.urls import path
from . import views

urlpatterns = [
    path('todos/<str:date>', views.TodosList.as_view(), name="todos"),
    path('todos/delete/<str:item_id>/<str:item_type>', views.TodosList.as_view(), name='delete-todo'),
    path('todos/edit/<str:item_id>/<str:item_type>', views.TodosList.as_view(), name='edit-todo'),
    path('all/status/<str:item_id>/<str:item_type>', views.AllStatusChange.as_view(), name="change-status"),
    path('week/list/<str:date>', views.WeekList.as_view(), name="week-list"),
    path('today/list/<str:todayDate>', views.TodayList.as_view(), name="today-list"),
    path('tasks/delete//<str:item_id>/<str:item_type>', views.TodayList.as_view(), name='delete-task'),
    path('tasks/', views.TaskList.as_view(), name="tasks"),
    path('tasks/delete/<str:item_id>/<str:item_type>', views.TaskList.as_view(), name="delete-task"),
    path('username/', views.UserInfo.as_view(), name="get-username"),
]