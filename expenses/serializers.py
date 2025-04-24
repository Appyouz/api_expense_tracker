from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserRegistrationSerializer(serializers.Serializer):
    """
    Serializer for user registration.
    Handles validation of username, email, password, and password confirmation.
    """
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)


    # Overriding the validate method (intended behavior)
    def validate(self, data): # type: ignore
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        return data

    def create(self, validated_data):
        """
        Create and return a new user instance, given the validated data.
        """
        # Remove password2 as we dont need to store it
        validated_data.pop('password2')

        # Create the user using Django's create_user method, which handles password hashing
        user = User.objects.create_user( # type: ignore
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
        )

        return user
