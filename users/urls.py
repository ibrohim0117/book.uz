from django.urls import path, include
from .views import UserRegisterView, UserLoginApiView, UserCheckApiView



urlpatterns = [
    path('sign-up/', UserRegisterView.as_view(), name='register'),
    path('sign-in/', UserLoginApiView.as_view(), name='login'),
    path('code/', UserCheckApiView.as_view(), name='code'),
]
