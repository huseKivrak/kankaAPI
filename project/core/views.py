from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status

from .models import User, Letter
from .serializers import MyTokenObtainPairSerializer, LetterSerializer, UserSerializer

###################
'''User Views'''
###################


class RegisterView(APIView):
    """
    Register a new user.
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class AllUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


###################
'''Letter Views'''
###################


class LetterList(ListCreateAPIView):
    """
    Retrieve all letters owned by the user:
    - all drafts
    - all received letters that have been delivered or read
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LetterSerializer


    def get_queryset(self):
        user = self.request.user
        queryset = Letter.objects.filter(owner=user)
        return queryset

    def post(self, request, *args, **kwargs):
        title = request.data.get('title')
        body = request.data.get('body')
        recipient_username = request.data.get('recipient')
        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            return Response(
                {'error': 'Recipient does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        draft = Letter.objects.create_draft(
            title=title,
            body=body,
            author=request.user,
            recipient=recipient,
        )

        serializer = self.get_serializer(draft)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LetterDetail(RetrieveUpdateDestroyAPIView):

    """
    Retrieve, update or delete a letter.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LetterSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Letter.objects.filter(owner=user)
        return queryset

    def patch(self, request, *args, **kwargs):
        letter = self.get_object()

        if letter.status == 'draft':
            serializer = self.get_serializer(data=request.data, partial=True)

            if serializer.is_valid():
                valid_data = serializer.validated_data
                if "title" in valid_data:
                    letter.title = valid_data["title"]
                if "body" in valid_data:
                    letter.body = valid_data["body"]
                letter.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(
                {'error': 'You can only update a draft letter.'},
                status=status.HTTP_400_BAD_REQUEST
            )
