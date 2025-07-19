from django.urls import path, include
from .views import UserRegisterView



urlpatterns = [
    path('sign-up/', UserRegisterView.as_view(), name='register'),
]
