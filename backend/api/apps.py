from django.apps import AppConfig
from .services.ScheduleManager import ScheduleManager
from .Dynamo import DynamoDB_Manager
import os


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        pass