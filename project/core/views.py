from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
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
    GET:
    Retrieve all user-owned letters:
    - all their drafts
    - all received letters ('delivered' or 'read', where user is recipient)

    POST:
    Create a new letter draft or send a letter.

    Request body:
    {
        "action": "save" | "send"
        "title": "string",
        "body": "string",
        "recipient": "string"
    }

    If action is "save", create a new draft letter.
    If action is "send", create and send letter.

    Response body:
    {
        "id": "integer",
        "status": "draft" | "sent" | "delivered" | "read",
        "delivery_date": null or "string",
        "title": "string",
        "body": "string",
        "author": "string",
        "recipient": "string",
        "owner": "string"
    }

    """

    permission_classes = [IsAuthenticated]
    serializer_class = LetterSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Letter.letters.filter(owner=user)
        return queryset

    def post(self, request, *args, **kwargs):
        title = request.data.get('title')
        body = request.data.get('body')
        recipient_username = request.data.get('recipient')
        action = request.data.get('action')

        if action not in ['save', 'send']:
            return Response(
                {'error': 'Invalid action (must be "save" or "send").'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            return Response(
                {'error': 'Recipient does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        letter = Letter.letters.create(
            title=title,
            body=body,
            author=request.user,
            recipient=recipient,
        )

        if action == 'save':
            serializer = self.get_serializer(letter)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif action == 'send':
            letter.send()
            serializer = self.get_serializer(letter)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LetterDetail(RetrieveUpdateAPIView):

    """
    GET:
    Retrieve a user-owned letter by id.

    PATCH:
    Edit a draft (action = "save" or send an existing one("send").
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LetterSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Letter.letters.filter(owner=user)
        return queryset

    def get(self, request, *args, **kwargs):
        letter = self.get_object()
        letter.mark_as_read()
        serializer = self.get_serializer(letter)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        letter = self.get_object()
        action = request.data.get('action')

        if action not in ['save', 'send']:
            return Response(
                {'error': 'Invalid action (must be "save" or "send").'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if letter.status != 'draft':
            return Response(
                {'error': 'Only drafts can be edited.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if action == 'save':
            serializer = self.get_serializer(
                data=request.data, partial=True)

            if serializer.is_valid():
                valid_data = serializer.validated_data
                if "title" in valid_data:
                    letter.title = valid_data["title"]
                if "body" in valid_data:
                    letter.body = valid_data["body"]
                letter.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        letter.send()
        serializer = self.get_serializer(letter)
        return Response(serializer.data, status=status.HTTP_200_OK)
