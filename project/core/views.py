from django.db.models import Q

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Letter
from .serializers import LetterSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for the token obtain pair view.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LetterList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LetterSerializer

    '''All user's drafts and received letters'''
    def get_queryset(self):
        user = self.request.user
        queryset = Letter.objects.filter(
            Q(author=user, status='draft') | Q(
                recipient__user=user, status__in=['delivered', 'read']
            ))
        return queryset

