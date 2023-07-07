from rest_framework import serializers
from .models import User, Letter




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = '__all__'
