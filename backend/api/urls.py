from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.Todos.as_view(), name="todos")
]