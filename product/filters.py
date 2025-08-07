from rest_framework import generics
from django_filters import rest_framework as filters
from .models import Book


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['name']