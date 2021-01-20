from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import GenericAPIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from teams.models import Team, Agency
from users.models import User
from common.models import CommonParameters
from common.serializers import IsSuperUser, IsAgencyAdmin, IsTeamLead, serialize_user
from .serializers import GetUserByIdSerializer, SingleAddUserSerializer, BulkAddUserSerializer, UserUpdateSerializer,\
    BasicInfoSerializer, GeneralInfoSerializer


class BasicInfoView(GenericAPIView):
    serializer_class = BasicInfoSerializer

    def get(self, request):
        user = request.user
        common_parameter = user.common_parameters
        return Response(
            {
                "result": True,
                "data": {
                    "user_info": {
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "phone_number": user.phone_number,
                        "email_address": user.email,
                        "currency": common_parameter.currency,
                        "date_type": common_parameter.date_type
                    }
                }
            }
        )

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        first_name = serializer.data.get('first_name')
        last_name = serializer.data.get('last_name')
        phone_number = serializer.data.get('phone_number')
        email_address = serializer.data.get('email_address')
        currency = serializer.data.get('currency')
        date_type = serializer.data.get('date_type')
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.email = email_address
        user.save()
        user.common_parameters.currency = currency
        user.common_parameters.date_type = date_type
        user.common_parameters.save()

        return Response(
            {
                "result": True,
                "data": {
                    "user_info": {
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "phone_number": user.phone_number,
                        "email_address": user.email,
                        "currency": user.common_parameters.currency,
                        "date_type": user.common_parameters.date_type
                    }
                }
            }
        )


class GeneralInfoView(GenericAPIView):
    serializer_class = GeneralInfoSerializer

    def get(self, request):
        user = request.user
        agency = user.agency
        common_parameter = agency.common_parameters
        return Response(
            {
                "result": True,
                "data": {
                    "user_info": {
                        "name": agency.name,
                        "currency": common_parameter.currency,
                        "date_type": common_parameter.date_type
                    }
                }
            }
        )

    def put(self, request):
        if not request.user.is_agency_admin:
            print('llllllllllllll')
            return Response(
                {
                    "result": False
                },
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.data.get('name')
        currency = serializer.data.get('currency')
        date_type = serializer.data.get('date_type')
        agency = request.user.agency
        agency.name = name
        agency.save()
        agency.common_parameters.currency = currency
        agency.common_parameters.date_type = date_type
        agency.common_parameters.save()

        return Response(
            {
                "result": True,
                "data": {
                    "user_info": {
                        "name": agency.name,
                        "currency": agency.common_parameters.currency,
                        "date_type": agency.common_parameters.date_type
                    }
                }
            }
        )


class UserDetailView(GenericAPIView):
    serializer_class = GetUserByIdSerializer

    def get(self, request, pk):
        serializer = self.get_serializer(data={"user_id": pk})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.team is None:
            team_name = None
            team_id = None
        else:
            team_name = user.team.name
            team_id = user.team.id
        return Response(
            {
                "result": True,
                "data": {
                    "user": {
                        **serialize_user(user),
                        "email": user.email,
                        "phone_number": user.phone_number,
                        "status": user.is_active,
                        "team_id": team_id,
                        "team_name": team_name,
                        "role": "Team Lead"
                    }
                },
            },
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, pk):
        try:
            User.objects.get(id=pk).delete()

            return Response(
                {
                    "result": True,
                    "data": {
                        "msg": "User removed successfully."
                    }
                }
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "result": False,
                    "errorCode": 1,
                    "errorMsg": "Invalid user id."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SearchDetailView(GenericAPIView):
    permission_classes = IsTeamLead,

    def get(self, request):
        keyword = request.GET.get('keyword')
        page = request.GET.get('page')
        number_per_page = request.GET.get('per_page')
        sort_by = request.GET.get('sort_by')
        sort_order = request.GET.get('sort_order')
        sea_users = []
        if request.user.is_superuser:
            if keyword:
                allusers = User.objects.filter(username__icontains=keyword).order_by('-id')
                number_of_active_users = User.objects.filter(username__icontains=keyword).count()
            else:
                allusers = User.objects.all().order_by('-id').order_by('-id')
                number_of_active_users = User.objects.all().count()
            paginator = Paginator(allusers, number_per_page)
            try:
                search = paginator.page(page)
            except PageNotAnInteger:
                search = paginator.page(1)
            except EmptyPage:
                search = []

        elif request.user.is_agency_admin:
            agency = request.user.agency
            if keyword:
                allusers = User.objects.filter(agency=agency, username__icontains=keyword).order_by('-id')
                number_of_active_users = User.objects.filter(agency=agency, username__icontains=keyword).count()
            else:
                allusers = User.objects.filter(agency=agency).order_by('-id').order_by('-id')
                number_of_active_users = User.objects.filter(agency=agency).count()
            paginator = Paginator(allusers, number_per_page)
            try:
                search = paginator.page(page)
            except PageNotAnInteger:
                search = paginator.page(1)
            except EmptyPage:
                search = []

        else:
            team = request.user.team
            if keyword:
                allusers = User.objects.filter(team=team, username__icontains=keyword).order_by('-id')
                number_of_active_users = User.objects.filter(team=team, username__icontains=keyword).count()
            else:
                allusers = User.objects.filter(team=team).order_by('-id').order_by('-id')
                number_of_active_users = User.objects.filter(team=team).count()
            paginator = Paginator(allusers, number_per_page)
            try:
                search = paginator.page(page)
            except PageNotAnInteger:
                search = paginator.page(1)
            except EmptyPage:
                search = []

        for sea in search:
            if sea.is_superuser:
                role = "Super User"
            elif sea.is_agency_admin:
                role = "Agency Admin"
            elif sea.is_team_lead:
                role = "Team Lead"
            else:
                role = "Agent"                
            if sea.team is None:
                team_name = None
                team_id = None
            else:
                team_name = sea.team.name
                team_id = sea.team.id
            if sea.agency is None:
                agency_name = None
                agency_id = None
            else:
                agency_name = sea.agency.name
                agency_id = sea.agency.id
            sea_users.append({
                **serialize_user(sea),
                "email": sea.email,
                "phone_number": sea.phone_number,
                "agency_id": agency_id,
                "agency_name": agency_name,
                "team_id": team_id,
                "team_name": team_name,
                "is_active": sea.is_active,
                "role": role
            })
        return Response(
            {
                "result": True,
                "data": {
                    "number_of_users": number_of_active_users,
                    "users": sea_users
                }
            },
            status=status.HTTP_201_CREATED
        )


class AddUserView(GenericAPIView):
    permission_classes = IsTeamLead,
    serializer_class = SingleAddUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User()
        user.email = serializer.data.get('email')
        user.username = serializer.data.get('first_name') + " " + serializer.data.get('last_name')
        user.first_name = serializer.data.get('first_name')
        user.last_name = serializer.data.get('last_name')
        if serializer.data.get('password'):
            user.password = serializer.data.get('password')
        user.is_active = serializer.data.get('is_active')
        if request.user.is_agency_admin:
            agency = request.user.agency
            common_parameter = agency.common_parameters
            common_parameters = CommonParameters()
            common_parameters.currency = common_parameter.currency
            common_parameters.date_type = common_parameter.date_type
            common_parameters.booking_enabled = common_parameter.booking_enabled
            common_parameters.virtual_interlining = common_parameter.virtual_interlining
            common_parameters.exclude_carriers = common_parameter.exclude_carriers
            common_parameters.save()
            user.agency = agency
            user.common_parameters = common_parameters
            if serializer.data.get('team_id'):
                try:
                    team = Team.objects.get(id=serializer.data.get('team_id'))
                    user.team = team
                    user.is_agent = False
                except ObjectDoesNotExist:
                    return Response(
                        {
                            "result": False,
                            "data": {
                                "msg": "Invalid team_id."
                            },
                        },
                    )
            else:
                user.is_agent = True
            user.save()
        elif request.user.is_team_lead:
            team = request.user.team
            user.team = team
            common_parameter = team.agency.common_parameters
            common_parameters = CommonParameters()
            common_parameters.currency = common_parameter.currency
            common_parameters.date_type = common_parameter.date_type
            common_parameters.booking_enabled = common_parameter.booking_enabled
            common_parameters.virtual_interlining = common_parameter.virtual_interlining
            common_parameters.exclude_carriers = common_parameter.exclude_carriers
            common_parameters.save()
            user.common_parameters = common_parameters
            user.agency = team.agency
            user.is_agent = False
            user.save()
        else:
            if serializer.data.get('agency_id'):
                try:
                    agency = Agency.objects.get(id=serializer.data.get('agency_id'))
                    user.agency = agency
                    common_parameter = agency.common_parameters
                    common_parameters = CommonParameters()
                    common_parameters.currency = common_parameter.currency
                    common_parameters.date_type = common_parameter.date_type
                    common_parameters.booking_enabled = common_parameter.booking_enabled
                    common_parameters.virtual_interlining = common_parameter.virtual_interlining
                    common_parameters.exclude_carriers = common_parameter.exclude_carriers
                    common_parameters.save()
                    user.common_parameters = common_parameters
                    user.is_agent = False
                except ObjectDoesNotExist:
                    return Response(
                        {
                            "result": False,
                            "data": {
                                "msg": "Invalid agency_id."
                            },
                        },
                    )
            if serializer.data.get('team_id'):
                try:
                    team = Team.objects.get(id=serializer.data.get('team_id'))
                    user.team = team
                    user.is_agent = False
                except ObjectDoesNotExist:
                    return Response(
                        {
                            "result": False,
                            "data": {
                                "msg": "Invalid team_id."
                            },
                        },
                    )
            else:
                user.is_agent = True
            user.save()

        return Response(
            {
                "result": True,
                "data": {
                    "msg": "Single User created."
                },
            },
        )


class AllUsersListView(GenericAPIView):
    permission_classes = IsTeamLead,

    def get(self, request):
        user_list = User.objects.filter(is_agent=True)
        user_detail = []
        for user in user_list:
            user_detail.append({
                **serialize_user(user)
            })
        return Response(
            {
                "result": True,
                "data": {
                    "users": user_detail
                }
            },
            status=status.HTTP_201_CREATED
        )


class AvailableUsersListView(GenericAPIView):
    permission_classes = IsTeamLead,

    def get(self, request, pk):
        team = Team.objects.get(id=pk)
        user_list = User.objects.filter(Q(is_agent=True) | Q(team=team))
        user_detail = []
        for user in user_list:
            user_detail.append({
                **serialize_user(user)
            })
        return Response(
            {
                "result": True,
                "data": {
                    "users": user_detail
                }
            },
            status=status.HTTP_201_CREATED
        )


class AvailableAdminListView(GenericAPIView):
    permission_classes = IsSuperUser,

    def get(self, request, pk):
        agency = Agency.objects.get(id=pk)
        user_list = User.objects.filter(Q(is_agent=True) | Q(agency=agency))
        user_detail = []
        for user in user_list:
            user_detail.append({
                **serialize_user(user)
            })
        return Response(
            {
                "result": True,
                "data": {
                    "users": user_detail
                }
            },
            status=status.HTTP_201_CREATED
        )


class BulkAddUserView(GenericAPIView):
    permission_classes = IsTeamLead,
    serializer_class = BulkAddUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        emails = serializer.data.get('emails')
        password = None
        if serializer.data.get('password'):
            password = serializer.data.get('password')
        if request.user.is_agency_admin:
            agency = request.user.agency
            common_parameter = agency.common_parameters
            if serializer.data.get('team_id'):
                try:
                    team = Team.objects.get(id=serializer.data.get('team_id'))
                    if emails:
                        for email in emails:
                            user = User()
                            user.email = email
                            user.username = email
                            user.first_name = email
                            user.last_name = email
                            user.team = team
                            user.agency = agency
                            user.password = password
                            user.is_active = serializer.data.get('is_active')
                            user.is_agent = True
                            common_parameters = CommonParameters()
                            common_parameters.currency = common_parameter.currency
                            common_parameters.date_type = common_parameter.date_type
                            common_parameters.booking_enabled = common_parameter.booking_enabled
                            common_parameters.virtual_interlining = common_parameter.virtual_interlining
                            common_parameters.exclude_carriers = common_parameter.exclude_carriers
                            common_parameters.save()
                            user.common_parameters = common_parameters
                            user.save()
                except ObjectDoesNotExist:
                    return Response(
                        {
                            "result": False,
                            "data": {
                                "msg": "team_id is invalid."
                            },
                        },
                    )
            else:
                if emails:
                    for email in emails:
                        user = User()
                        user.email = email
                        user.username = email
                        user.first_name = email
                        user.last_name = email
                        user.password = password
                        user.agency = agency
                        user.is_agent = True
                        user.is_active = serializer.data.get('is_active')
                        common_parameters = CommonParameters()
                        common_parameters.currency = common_parameter.currency
                        common_parameters.date_type = common_parameter.date_type
                        common_parameters.booking_enabled = common_parameter.booking_enabled
                        common_parameters.virtual_interlining = common_parameter.virtual_interlining
                        common_parameters.exclude_carriers = common_parameter.exclude_carriers
                        common_parameters.save()
                        user.common_parameters = common_parameters
                        user.save()
        elif request.user.is_team_lead:
            team = request.user.team
            agency = team.agency
            common_parameter = agency.common_parameters
            if emails:
                for email in emails:
                    user = User()
                    user.email = email
                    user.username = email
                    user.first_name = email
                    user.last_name = email
                    user.team = team
                    user.agency = agency
                    user.password = password
                    user.is_active = serializer.data.get('is_active')
                    user.is_agent = True
                    common_parameters = CommonParameters()
                    common_parameters.currency = common_parameter.currency
                    common_parameters.date_type = common_parameter.date_type
                    common_parameters.booking_enabled = common_parameter.booking_enabled
                    common_parameters.virtual_interlining = common_parameter.virtual_interlining
                    common_parameters.exclude_carriers = common_parameter.exclude_carriers
                    common_parameters.save()
                    user.common_parameters = common_parameters
                    user.save()
        else:
            try:
                agency = Agency.objects.get(id=serializer.data.get('agency_id'))
                common_parameter = agency.common_parameters

                if serializer.data.get('team_id'):
                    try:
                        team = Team.objects.get(id=serializer.data.get('team_id'))
                        if emails:
                            for email in emails:
                                user = User()
                                user.email = email
                                user.username = email
                                user.first_name = email
                                user.last_name = email
                                user.agency = agency
                                user.team = team
                                user.password = password
                                user.is_agent = True
                                user.is_active = serializer.data.get('is_active')
                                common_parameters = CommonParameters()
                                common_parameters.currency = common_parameter.currency
                                common_parameters.date_type = common_parameter.date_type
                                common_parameters.booking_enabled = common_parameter.booking_enabled
                                common_parameters.virtual_interlining = common_parameter.virtual_interlining
                                common_parameters.exclude_carriers = common_parameter.exclude_carriers
                                common_parameters.save()
                                user.common_parameters = common_parameters
                                user.save()
                    except ObjectDoesNotExist:
                        return Response(
                            {
                                "result": False,
                                "data": {
                                    "msg": "team_id is invalid."
                                },
                            },
                        )
                elif emails:
                    for email in emails:
                        user = User()
                        user.email = email
                        user.username = email
                        user.first_name = email
                        user.last_name = email
                        user.agency = agency
                        user.password = password
                        user.is_active = serializer.data.get('is_active')
                        user.is_agent = True
                        common_parameters = CommonParameters()
                        common_parameters.currency = common_parameter.currency
                        common_parameters.date_type = common_parameter.date_type
                        common_parameters.booking_enabled = common_parameter.booking_enabled
                        common_parameters.virtual_interlining = common_parameter.virtual_interlining
                        common_parameters.exclude_carriers = common_parameter.exclude_carriers
                        common_parameters.save()
                        user.common_parameters = common_parameters
                        user.save()
            except ObjectDoesNotExist:
                return Response(
                    {
                        "result": False,
                        "data": {
                            "msg": "agency_id is invalid."
                        },
                    },
                )

        return Response(
            {
                "result": True,
                "data": {
                    "msg": "Bulk Users created."
                },
            },
        )


class EmailCheckView(GenericAPIView):

    def get(self, request):
        email = request.GET.get('email')
        if User.objects.filter(email=email).exists():
            return Response(
                {
                    "result": False,
                    "data": {
                        "msg": "Email duplicated."
                    },
                },
            )

        return Response({"result": True})


class UserUpdateView(GenericAPIView):
    serializer_class = UserUpdateSerializer

    def put(self, request):
        team_id = team_name = agency_id = agency_name = None
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.first_name = serializer.data.get('first_name')
        user.last_name = serializer.data.get('last_name')
        user.email = serializer.data.get('email')
        user.phone_number = serializer.data.get('phone_number')
        user.is_active = serializer.data.get('is_active')
        if serializer.data.get('team_id'):
            user.team = Team.objects.get(id=serializer.data.get('team_id'))
            team_id = user.team.id
            team_name = user.team.name
        if serializer.data.get('agency_id'):
            user.agency = Agency.objects.get(id=serializer.data.get('agency_id'))
            agency_id = user.agency.id
            agency_name = user.agency.name
        user.save()
        if not user.team:
            team_id = None
            team_name = None
        if not user.agency:
            agency_id = None
            agency_name = None

        return Response(
            {
                "result": True,
                "data": {
                    "user": {
                        **serialize_user(user),
                        "email": user.email,
                        "phone_number": user.phone_number,
                        "is_active": user.is_active,
                        "team_id": team_id,
                        "team_name": team_name,
                        "agency_id": agency_id,
                        "agency_name": agency_name,
                        "role": "Team Lead"
                    }
                }
            },
            status=status.HTTP_201_CREATED
        )


class UserAchieveView(GenericAPIView):
    permission_classes = IsTeamLead,

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            if user.is_active:
                user.is_active = False
                user.save()
            else:
                user.is_active = True
                user.save()
            return Response(
                {
                    "result": True,
                    "data": {
                        "msg": "User archived."
                    },
                },
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "result": False,
                    "data": {
                        "msg": "User archive failed."
                    },
                },
            )
