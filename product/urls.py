from django.contrib import admin
from django.urls import path

from .views import CategoryListAPIView, BookListAPIView, CategoryCreateAPIView, BookCreateAPIView


urlpatterns = [
    path('category-list/', CategoryListAPIView.as_view(), name='category-list'),
    path('category-create/', CategoryCreateAPIView.as_view(), name='category-create'),

    path('book-list/', BookListAPIView.as_view(), name='book-list'),
    path('book-create/', BookCreateAPIView.as_view(), name='book-create'),
]
