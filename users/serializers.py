from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .models import User
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate


class UserRegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone=validated_data.get('phone'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        user.create_code()
        return user
    
    def to_representation(self, instance):
        instance = super().to_representation(instance)
        phone = instance.get('phone')
        user = User.objects.filter(phone=phone)
        if user.exists():
            token = user.first().token()
            instance['tokens'] = token
        # print(instance)
        return instance
    

class UserLoginSerializer(TokenObtainPairSerializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        user = User.objects.filter(phone=phone).first()
        if not user:
            raise ValidationError({'message': 'Bunday foydalanuvchi mavjud emas!'})

        auth_user = authenticate(phone=user.phone, password=password)
        if auth_user is None:
            raise ValidationError({'message': 'Telefon raqam yoki parol noto‘g‘ri!'})

        # if not auth_user.is_verified:
        #     raise ValidationError({'message': "Siz hali ro'yhatdan to'liq o'tmagansiz!"})

        token_data = super().get_token(auth_user)
        data = {
            'phone': phone,
            'access': str(token_data.access_token),
            'refresh': str(token_data),
        }
        return data
        