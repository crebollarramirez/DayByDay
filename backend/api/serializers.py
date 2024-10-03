from rest_framework import serializers
from services import UserManager

class UserSerializer(serializers.Serializer):
    user_id = serializers.CharField(read_only=True)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user_manager = UserManager()
        user = user_manager.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        UserManager.store_user(user)  # Save user to DynamoDB
        return user