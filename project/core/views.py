from django.db.models import Q

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Letter
from .serializers import LetterSerializer

###################
'''User Auth Views'''
###################
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    add username to token
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




###################
'''Letter Views'''
###################


class LetterList(ListCreateAPIView):
    """
    Retrieve all letters relevant to the user:
    - all drafts
    - all received letters that have been delivered or read
    """

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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LetterDetail(RetrieveUpdateDestroyAPIView):

    """
    Retrieve, update or delete a letter.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LetterSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Letter.objects.filter(author=user)

        return queryset
