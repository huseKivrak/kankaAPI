from django.urls import path
from .views import MyTokenObtainPairView, LetterList, LetterDetail, LetterCreate
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('letters/', LetterList.as_view(), name='letter_list'),
    path('letters/<int:pk>/', LetterDetail.as_view(), name='letter_detail'),
    path('letters/create/', LetterCreate.as_view(), name='letter_create'),
]
