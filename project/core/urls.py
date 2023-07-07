from django.urls import path
from .views import RegisterView, AllUsersView, MyTokenObtainPairView, LetterList, LetterDetail
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('users/', AllUsersView.as_view(), name='all_users'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('letters/', LetterList.as_view(), name='letter_list_create'),
    path('letters/<int:pk>/', LetterDetail.as_view(), name='letter_detail'),
]
