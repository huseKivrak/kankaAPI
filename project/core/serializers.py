from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Letter


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    add username to token
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'zip_code']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = '__all__'
