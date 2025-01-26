from rest_framework import serializers
from django.contrib.auth import get_user_model

user_model = get_user_model()

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        user = user_model.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

