from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, permissions
import uuid
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_auth.views import LoginView, LogoutView
from datetime import datetime
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RegistrationSerializer, ForgotSerializer, ConfirmTokenSerializer, ResetPasswordSerializer, \
    ChangePasswordSerializer
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
                    "username": self.user.username,
                    "first_name": self.user.first_name,
                    "last_name": self.user.last_name,
                    "is_superuser": self.user.is_superuser,
                    "is_agent": self.user.is_agent,
                    "is_team_lead": self.user.is_team_lead,
                    "is_agency_admin": self.user.is_agency_admin
                }
            }
        }

        return Response(response, status=status.HTTP_201_CREATED)


class UserRegistrationView(CreateAPIView):
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
    serializer_class = ForgotSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = None

        username = serializer.data.get('username')
        print(username)
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}

        try:
            user = User.objects.get(**kwargs)
            print(user.username)
            if user.is_active:
                token = uuid.uuid4()
                print(token)
                user.password_reset_token = token
                user.password_reset_sent_at = datetime.now()
                user.save()
        except ObjectDoesNotExist:
            pass

        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "result": True,
                "data": {
                    "reset_token": token
                }
             }, status=status.HTTP_201_CREATED, headers=headers
        )


class ConfirmTokenView(CreateAPIView):

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        try:
            user = User.objects.get(password_reset_token=token)
            return Response({"result": True}, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response({"result": False}, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordView(CreateAPIView):

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        password = request.GET.get('password')
        try:
            user = User.objects.get(password_reset_token=token)
            user.password = make_password(password)
            user.password_reset_sent_at = None
            user.password_reset_token = None
            user.save()
            return Response({"result": True}, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response({"result": False}, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(CreateAPIView):
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


class UserDetailsView(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        user = request.user
        user_data = {
            'user_email': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_type': user.date_type,
            'currency': user.currency,
            'student_and_youth': user.student_and_youth,
            'pcc': user.pcc,
            'provider': user.provider,
            'agency': request.user.group,
            'ticketing_queue': request.user.queue,
            'is_group_admin': request.user.is_group_admin,
            'is_superuser': request.user.is_superuser,
            'booking_disabled': request.user.disable_booking,
            'virtual_interlining': request.user.virtual_interlining,
            'view_pnr_pricing': request.user.view_pnr_pricing,
            'markup_visible': request.user.markup_visible
        }
        return Response(user_data, status=status.HTTP_200_OK)

#class SearchFlightsView(CreateAPIView):
#    
#    def post(self, request):
#        search_result = search(request.user, request.data)
#        return Response(search_result, status=status.HTTP_200_OK)


#class PriceFlightsView(CreateAPIView):
#
#    def post(self, request):
#        price_result = price(request.user, request.data)
#        return Response(price_result, status=status.HTTP_200_OK)
