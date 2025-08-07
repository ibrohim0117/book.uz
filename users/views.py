from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from django.utils.timezone import now
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import User
from .serializers import (
    UserRegisterSerializer, UserLoginSerializer, CheckUserCodeSerializer,
    GetPhoneSerializer
)

@extend_schema(tags=['auth'])
class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer



@extend_schema(tags=["auth"])
class UserLoginApiView(TokenObtainPairView):
    serializer_class = UserLoginSerializer



class UserCheckApiView(APIView):

    @extend_schema(request=CheckUserCodeSerializer)
    def post(self, request):
        # user = self.request.user
        serializer = CheckUserCodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get('code')
            phone = serializer.validated_data.get('phone')
            user = User.objects.filter(phone=phone).first()
            if not user:
                raise ValidationError('Tel raqam xato!')
            
            print(self.check_code(user, code))

        return Response({
            'message': 'User tasdiqlandi!'
        })
    

    @staticmethod
    def check_code(user, code):                                         #10:13 < 10:14
        code_list = user.codes.filter(code=code, is_confirmed=False, expiration_time__gte=now())
        if not code_list.exists():
            # print(code_list.first())
            raise ValidationError({
                "message": "Code xato yokida eskirgan!"
            })
        
        code_list.update(is_confirmed=True)
        user.is_verified = True
        user.auth_status = User.AuthStatus.CODE_VERIFIED
        user.save()

        return True



class GetNewVerification(APIView):

    @extend_schema(request=GetPhoneSerializer)
    def post(self, request, *args, **kwargs):
        serializer = GetPhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get('phone')
            user = User.objects.filter(phone=phone).first()
            if not user:
                raise ValidationError("Telefon raqam xato!")
            
            self.check_verification(user)

            if not user.is_verified:
                user.create_code()
                return Response(
                    {
                        'success': True,
                        'message': 'Tasdiqlash kodingiz qaytadan yuborildi!'
                    }
                )

            raise ValidationError({'message': 'Foydalanuvchi allaqachon tasdiqlangan'}, code=400)

    @staticmethod
    def check_verification(user):
        verifies = user.codes.filter(expiration_time__gte=now(), is_confirmed=False)
        if verifies.exists():
            raise ValidationError({'message': 'Kodingiz hali ishlatish uchun yaroqli'}, code=400)


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUzODQ4NDM3LCJpYXQiOjE3NTM3NjIwMzcsImp0aSI6Ijg5ZmZjZGQxYTczYjQzMzE4ZGFhYjY5MDAyMThiOGRmIiwidXNlcl9pZCI6IjEyIn0.QAU5JKVjlkyXmIF71h8QIVJVhlPSvZMdshKncqBcJHY
    