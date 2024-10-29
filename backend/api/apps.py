from django.apps import AppConfig
from .services.ScheduleManager import ScheduleManager
from .Dynamo import DynamoDB_Manager
import os


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Run getData() only when RUN_MAIN is not set to prevent double execution during reload
        # DynamoDB_Manager().create_dynamodb_table()
        ScheduleManager().getData()
        print("SERVER RESTARTS")