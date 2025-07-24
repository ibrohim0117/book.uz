from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from .models import User
from .serializers import UserRegisterSerializer, UserLoginSerializer


@extend_schema(tags=['auth'])
class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer



@extend_schema(tags=["auth"])
class UserLoginApiView(TokenObtainPairView):
    serializer_class = UserLoginSerializer
