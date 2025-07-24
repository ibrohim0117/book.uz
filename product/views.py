from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from .models import Category, Book
from .serializers import CategorySerializer, BookSerializer


@extend_schema(tags=['category'])
class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(tags=['category'])
class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, )


@extend_schema(tags=['book'])
class BookListAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



@extend_schema(tags=['book'])
class BookCreateAPIView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

