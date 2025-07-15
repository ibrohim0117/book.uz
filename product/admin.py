from django.contrib import admin
from .models import Category, Author, Publisher, Book


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'id')
    search_fields = ('name', 'slug')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'id')
    search_fields = ('name', 'slug')



@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'id')
    search_fields = ('name', 'slug')



@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'language', 'author__name', 'publish__name', 'created_at')
    search_fields = ('name', 'slug', 'author', 'publish__name')
    list_filter = ('language', 'author', 'publish', 'created_at')
 


