from django.contrib.auth.backends import BaseBackend
from .services import UserManager

class DynamoDB_Backend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        return UserManager.authenticate_user(username, password)
    
    def get_user(self, username):
        return UserManager.get_user(username)