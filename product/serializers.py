from rest_framework.serializers import ModelSerializer, Serializer
from .models import Category, Book


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['name', 'slug', 'price', 'author', 'publish', 'language', 'id']



