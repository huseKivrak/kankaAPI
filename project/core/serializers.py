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
        fields = ['id', 'username', 'email', 'zip_code']

class LetterSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    recipient = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Letter
        fields = '__all__'
