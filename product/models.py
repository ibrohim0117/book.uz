import uuid
from django.db import models
from django.utils.text import slugify


class BaseCreatedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True



class Category(BaseCreatedModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if Category.objects.filter(slug=self.slug).exists():
            self.slug += uuid.uuid4().__str__().split('-')[-1]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    


class Author(BaseCreatedModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    


class Publisher(BaseCreatedModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    about = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    


class Book(BaseCreatedModel):

    class LanguageType(models.TextChoices):
        UZ = 'uz', 'Uzbekcha'
        RU = 'ru', 'Ruscha'
        EN = 'en', 'English'

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    price = models.IntegerField()
    about = models.TextField()
    image = models.ImageField(upload_to='books/')
    info = models.JSONField(default=dict)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='authors')
    publish = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='publisher')
    language = models.CharField(max_length=10, choices=LanguageType.choices)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if Book.objects.filter(slug=self.slug).exists():
            self.slug += uuid.uuid4().__str__().split('-')[-1]
        super().save(*args, **kwargs)

    


