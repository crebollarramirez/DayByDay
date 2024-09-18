from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Task


class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)


class NoteDelete(generics.DestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects


class CreateNoteView(generics.CreateAPIView):
    queryset = Task.objects.all()