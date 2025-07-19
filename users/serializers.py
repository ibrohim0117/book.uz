from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers
from .models import User


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
        