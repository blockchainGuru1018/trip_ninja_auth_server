from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import GenericAPIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from teams.models import Team, Agency
from users.models import User
from common.serializers import serialize_user
from .serializers import GetUserByIdSerializer, AddUserSerializer


class UserDetailView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = GetUserByIdSerializer

    def get(self, request, pk):
        serializer = self.get_serializer(data={"user_id": pk})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user == request.user:
            return Response(
                {
                    "result": True,
                    "data": {
                        "user": {
                            **serialize_user(user),
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "phone_number": user.phone_number,
                            "currency": user.common_parameters.currency,
                            "date_type": user.common_parameters.date_type,
                            "booking_enabled": user.common_parameters.booking_enabled
                        }
                    },
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    "result": True,
                    "data": {
                        "user": {
                            **serialize_user(user),
                        }
                    }
                },
                status=status.HTTP_201_CREATED
            )


class AllUserDetailView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user_list = User.objects.all()
        user_info = []
        for user in user_list:
            user_info.append({
                **serialize_user(user),
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone_number": user.phone_number,
                "currency": user.common_parameters.currency,
                "date_type": user.common_parameters.date_type,
                "booking_enabled": user.common_parameters.booking_enabled
            })

        return Response(
            {
                "result": True,
                "data": {
                    "user_list": user_info
                },
            },
            status=status.HTTP_201_CREATED
        )


class SearchDetailView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        keyword = request.GET.get('keyword')
        page = request.GET.get('page')
        number_per_page = request.GET.get('per_page')
        if keyword:
            allusers = User.objects.filter(username__icontains=keyword)
            number_of_active_users = User.objects.filter(username__icontains=keyword, is_active=True).count()
        else:
            allusers = User.objects.all()
            number_of_active_users = User.objects.filter(is_active=True).count()
        paginator = Paginator(allusers, number_per_page)
        try:
            search = paginator.page(page)
        except PageNotAnInteger:
            search = paginator.page(1)
        except EmptyPage:
            search = []

        sea_users = []
        for sea in search:
            sea_users.append({
                **serialize_user(sea),
            })
        return Response(
            {
                "result": True,
                "data": {
                    "number_of_active_users": number_of_active_users,
                    "users": sea_users
                }
            },
            status=status.HTTP_201_CREATED
        )


class AddUserView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = AddUserSerializer

    def post(self, request):
        is_possible = Agency.objects.filter(admin=request.user) | Team.objects.filter(admin=request.user) | \
                      request.user.is_superuser
        if not is_possible:
            return Response(
                {
                    "result": False,
                    "errorCode": 3,
                    "errorMsg": "You don't have the permission."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User()
        user.email = serializer.data.get('email')
        user.username = serializer.data.get('username')
        user.first_name = serializer.data.get('first_name')
        user.last_name = serializer.data.get('last_name')
        user.phone_number = serializer.data.get('phone_number')
        user.agency = serializer.validated_data['agency']
        user.team = serializer.validated_data['team']
        user.common_parameters = serializer.validated_data['common_parameter']
        user.is_active = serializer.data.get('is_active')
        user.is_superuser = serializer.data.get('is_superuser')
        user.is_agent = serializer.data.get('is_agent')
        user.is_team_lead = serializer.data.get('is_team_lead')
        user.is_agency_admin = serializer.data.get('is_agency_admin')
        user.save()

        return Response(
            {
                "result": True,
                "data": {
                    "user": {
                        **serialize_user(user),
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "phone_number": user.phone_number,
                        "agency": user.agency.name,
                        "team": user.team.name,
                        "is_active": user.is_active,
                        "is_agent": user.is_agent,
                        "is_team_lead": user.is_team_lead,
                        "is_agency_admin": user.is_agency_admin
                    }
                },
            },
        )