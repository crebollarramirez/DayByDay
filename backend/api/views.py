from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Task
from rest_framework.response import Response
from rest_framework import status


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
    
# class DeleteAllTasks(generics.DestroyAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     permission_classes = [AllowAny]

#     def delete(self, request, *args, **kwargs):
#         # Delete all tasks
#         self.queryset.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

