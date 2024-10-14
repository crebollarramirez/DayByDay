from django.apps import AppConfig
from .services import ScheduleManager
import os


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Run getData() only when RUN_MAIN is not set to prevent double execution during reload
        ScheduleManager().getData()
        print("SERVER RESTARTS")