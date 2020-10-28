from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_auth.views import LoginView, LogoutView
from datetime import datetime
import random

from .serializers import RegistrationSerializer, ForgotSerializer, ConfirmTokenSerializer, ResetPasswordSerializer, \
    ChangePasswordSerializer, SocialLoginSerializer
from users.models import User


class UserLoginView(LoginView):
    def get_response(self):
        original_response = super().get_response()

        response = {
            "result": True,
            "data": {
                "token": original_response.data.get('key'),
                "user": {
                    "id": self.user.id,
                    "email": self.user.email,
                    "user_type": self.user.user_type,
                    "username": self.user.username,
                    "first_name": self.user.first_name,
                    "last_name": self.user.last_name
                }
            }
        }

        return Response(response, status=status.HTTP_201_CREATED)


class UserRegistrationView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response({"result": True}, status=status.HTTP_201_CREATED, headers=headers)


class UserLogoutView(LogoutView):
    def logout(self, request):
        super().logout(request)
        return Response({"result": True}, status=status.HTTP_201_CREATED)


class ForgotPasswordView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ForgotSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data.get('username')
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}

        try:
            user = User.objects.get(**kwargs)
            if user.is_active:
                token = random.randint(100000, 999999)
                user.password_reset_token = token
                user.password_reset_sent_at = datetime.now()
                user.save()
        except ObjectDoesNotExist:
            pass

        headers = self.get_success_headers(serializer.data)
        return Response({"result": True}, status=status.HTTP_201_CREATED, headers=headers)


class ConfirmTokenView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ConfirmTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(password_reset_token=int(serializer.data.get('token')))
        user.password_reset_sent_at = None
        user.save()

        return Response({"result": True}, status=status.HTTP_201_CREATED)


class ResetPasswordView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(password_reset_token=int(serializer.data.get('token')))
        user.password = serializer.data.get('password')
        user.password_reset_token = None
        user.save()

        return Response({"result": True}, status=status.HTTP_201_CREATED)


class ChangePasswordView(CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = ChangePasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={
            'user_id': request.user.id,
            'current_password': request.data.get('current_password'),
            'new_password': request.data.get('new_password')
        })
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.password = serializer.data.get('new_password')
        user.save()

        return Response({"result": True}, status=status.HTTP_200_OK)


class SocialLoginView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = SocialLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_info = serializer.validated_data['user_info']
        provider = serializer.data.get('provider')
        try:
            user = User.objects.get(email=user_info['email'])
        except ObjectDoesNotExist:
            user = User()
            if provider == 'google':
                user.email = user_info['email']
                user.username = user_info['name']
                user.email_confirmed = True
            elif provider == 'facebook':
                user.email = user_info['email']
                user.username = user_info['name']
                user.email_confirmed = True
            user.save()

        if not user.is_active:
            return Response(
                {
                    "result": False,
                    "errorCode": 13,
                    "errorMsg": "User account is disabled."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        response = {
            "result": True,
            "data": {
                "user": {
                    "user_id": user.id,
                    "email": user.email,
                    "username": user.username,
                }
            }
        }

        return Response(response, status=status.HTTP_201_CREATED)
