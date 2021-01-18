from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, permissions
from django.conf import settings
import uuid
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_auth.views import LogoutView
from datetime import datetime
from django.contrib.auth.hashers import make_password
from .serializers import RegistrationSerializer, ForgotSerializer, ChangePasswordSerializer
from users.models import User
from api.service import add_common_parameters, send_api_request, get_user_queue
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

class UserSettingsView(GenericAPIView):
    def post(self, request):
        user = request.user

        response = {
            "result": True,
            "data": {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_superuser": user.is_superuser,
                    "is_agent": user.is_agent,
                    "is_team_lead": user.is_team_lead,
                    "is_agency_admin": user.is_agency_admin
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
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}

        try:
            user = User.objects.get(**kwargs)
            if user.is_active:
                token = uuid.uuid4()
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

class UserDetailsView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        user = request.user
        user_data = {
            'user_email': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_type': user.common_parameters.date_type,
            'currency': user.common_parameters.currency,
            'student_and_youth': user.agency.student_and_youth,
            'agency': user.agency.name,
            'ticketing_queue': get_user_queue(user), #TODO this should moved to credentials obj for multi-datasource bookings
            'is_agency_admin': user.is_agency_admin,
            'is_superuser': user.is_superuser,
            'booking_enabled': user.common_parameters.booking_enabled,
            'virtual_interlining': user.common_parameters.virtual_interlining,
            'view_pnr_pricing': user.common_parameters.view_pnr_pricing,
            'markup_visible': user.common_parameters.markup_visible
        }
        return Response(user_data, status=status.HTTP_200_OK)


class SearchFlightsView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    method_decorator(csrf_protect)

    def post(self, request):
        url = settings.API_URL + 'search/' + request.user.search_endpoint + '/'
        search_request = add_common_parameters(request.data, request.user)
        search_result = send_api_request('POST', url, request.user, search_request)
        return Response(search_result, status=status.HTTP_200_OK)


class PriceMapView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    method_decorator(csrf_protect)
    def post(self, request):
        url = settings.API_URL + 'price-map/'
        price_map_response = send_api_request('GET', url, request.user, request.data)
        return Response(price_map_response, status=status.HTTP_200_OK)


class PriceFlightsView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    method_decorator(csrf_protect)
    def post(self, request):
        url = settings.API_URL + 'price/' + request.user.search_endpoint + '/'
        price_result = send_api_request('POST', url, request.user, request.data)
        return Response(price_result, status=status.HTTP_200_OK)


class BookView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    method_decorator(csrf_protect)
    def post(self, request):
        url = settings.API_URL + 'book/' + request.user.booking_endpoint + '/'
        book_request = request.data
        book_request['consolidate_ticket'] = request.user.common_parameters.consolidate_ticket
        book_result = send_api_request('POST', url, request.user, book_request)
        return Response(book_result, status=status.HTTP_200_OK)


class QueueView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    method_decorator(csrf_protect)
    def post(self, request):
        url = settings.API_URL + 'queue/'
        response = send_api_request('POST', url, request.user, request.data)
        return Response(response, status=status.HTTP_200_OK)


class TicketView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    method_decorator(csrf_protect)
    def post(self, request):
        url = settings.API_URL + 'ticket/'
        response = send_api_request('POST', url, request.user, request.data)
        return Response(response, status=status.HTTP_200_OK)


class CancelView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    method_decorator(csrf_protect)
    def post(self, request):
        url = settings.API_URL + 'book/'
        response = send_api_request('DELETE', url, request.user, request.data)
        return Response(response, status=status.HTTP_200_OK)


class BookingsListView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    method_decorator(csrf_protect)
    def get(self, request):
        url = settings.API_URL + request.get_full_path()[8:]
        booking_list = send_api_request('GET', url, request.user, request.data)
        return Response(booking_list, status=status.HTTP_200_OK)


class BookingDetailsView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    method_decorator(csrf_protect)
    def get(self, request):
        url = settings.API_URL + request.get_full_path()[8:]
        booking_detail = send_api_request('GET', url, request.user, request.data)
        return Response(booking_detail, status=status.HTTP_200_OK)

