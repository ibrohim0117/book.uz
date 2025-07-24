import random
import uuid
from datetime import timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


NEW = 'new'
CODE_VERIFIED = 'code_verified'



class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The phone number field must be set')

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):

    class RoleType(models.TextChoices):
        USERS= 'user', 'User'
        ADMIN = 'admin', 'Admin'


    class AuthStatus(models.TextChoices):
        NEW = 'new', 'New'
        CODE_VERIFIED = 'code_verified', 'Code Verified'




    role = models.CharField(max_length=10, choices=RoleType.choices, default=RoleType.USERS)
    auth_status = models.CharField(max_length=20, choices=AuthStatus.choices, default=AuthStatus.NEW)


    birthday = models.DateField(blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+998\d{9}$|^\d{9}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 25 digits allowed.")
    
    phone = models.CharField(max_length=15, unique=True, validators=[phone_regex])


    image = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    is_verified = models.BooleanField(default=False)

    email = models.EmailField(unique=True, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []


    username = None


    def create_code(self):
        code = "".join([str(random.randint(1, 9)) for _ in range(6)])
        UserConfirmation.objects.create(
            code=code,
            user_id=self.id
        )
        return code

    def token(self):
        refresh = RefreshToken.for_user(self)
        data = {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token)
        }
        return data


    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


class UserConfirmation(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='codes')
    code = models.CharField(max_length=6)
    expiration_time = models.DateTimeField(blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expiration_time:
            self.expiration_time = timezone.now() + timedelta(minutes=3)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Tasdiqlash kodi'
        verbose_name_plural = 'Tasdiqlash kodlari'