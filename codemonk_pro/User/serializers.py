from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ("id", "email", "name", "date_of_birth", "password")
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            date_of_birth=validated_data["date_of_birth"],
            password=validated_data["password"],
        )
        return user
