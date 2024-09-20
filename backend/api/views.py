from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Task


class TaskListCreate(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Task.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)


class TaskDelete(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Task.objects.all()

