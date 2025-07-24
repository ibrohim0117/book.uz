from django.urls import path, include
from .views import UserRegisterView, UserLoginApiView



urlpatterns = [
    path('sign-up/', UserRegisterView.as_view(), name='register'),
    path('sign-in/', UserLoginApiView.as_view(), name='login'),
]
