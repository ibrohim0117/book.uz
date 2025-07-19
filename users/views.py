from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserRegisterSerializer


@extend_schema(tags=['auth'])
class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

