from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.db.models import Q

from common.serializers import serialize_team, serialize_agency
from teams.models import Team, Agency, DataSource
from users.models import User
from .serializers import TeamCreateSerializer, AgencySerializer, TeamSerializer, TeamUpdateSerializer, \
    AgencyAddSerializer, AgencyUpdateSerializer


class AllTeamsView(GenericAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = ()

    def get(self, request):
        keyword = request.GET.get('keyword')
        page = request.GET.get('page')
        number_per_page = request.GET.get('per_page')
        if keyword:
            allteams = Team.objects.filter(name__icontains=keyword).order_by('-id')
            number_of_team = Team.objects.filter(name__icontains=keyword).count()
        else:
            allteams = Team.objects.all().order_by('-id')
            number_of_team = Team.objects.all().count()
        paginator = Paginator(allteams, number_per_page)
        try:
            search = paginator.page(page)
        except PageNotAnInteger:
            search = paginator.page(1)
        except EmptyPage:
            search = []

        sea_teams = []
        for sea in search:
            number_of_users = User.objects.filter(team=sea).count()
            members = User.objects.filter(team=sea).values_list("id", flat=True)
            sea_teams.append({
                **serialize_team(sea),
                "leader_id": sea.admin.id,
                "is_booking": sea.is_booking,
                "members": members,
                "number_of_users": number_of_users
            })
        return Response(
            {
                "result": True,
                "data": {
                    "number_of_teams": number_of_team,
                    "teams": sea_teams
                }
            },
            status=status.HTTP_201_CREATED
        )


class AllTeamsListView(GenericAPIView):

    def get(self, request):
        team_list = Team.objects.all()
        team_detail = []
        for team in team_list:
            team_detail.append({
                **serialize_team(team)
            })
        return Response(
            {
                "result": True,
                "data": {
                    "teams": team_detail
                }
            },
            status=status.HTTP_201_CREATED
        )


class TeamDetailView(GenericAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = ()
    serializer_class = TeamSerializer

    def get(self, request, pk):
        serializer = self.get_serializer(data={"team_id": pk})
        serializer.is_valid(raise_exception=True)
        team = serializer.validated_data['team']
        members = User.objects.filter(team=team).values_list('id', flat=True)

        return Response(
            {
                "result": True,
                "data": {
                    "team_name": team.name,
                    "is_booking": team.is_booking,
                    "team_lead": team.admin.username,
                    "members": members
                }
            }
        )

    def delete(self, request, pk):
        try:
            is_agency_admin = Agency.objects.filter(admin=request.user).exists()
            is_permission = is_agency_admin | request.user.is_superuser
            if not is_permission:
                return Response(
                    {
                        "result": False,
                        "errorCode": 3,
                        "errorMsg": "You don't have the permission."
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            Team(id=pk).delete()

            return Response(
                {
                    "result": True,
                    "data": {
                        "msg": "Team removed successfully."
                    }
                }
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "result": False,
                    "errorCode": 1,
                    "errorMsg": "Invalid team id."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TeamUpdateView(GenericAPIView):
    serializer_class = TeamUpdateSerializer

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = serializer.validated_data['team']
        team.admin = serializer.validated_data['team_lead']
        team.is_booking = serializer.data.get('is_booking')
        team.name = serializer.data.get('team_name')
        team.save()
        members = serializer.data.get('members')
        if members:
            User.objects.filter(team=team).update(team=None, is_agent=True)
            User.objects.filter(id__in=members).update(team=team, is_agent=False)
        number_of_users = User.objects.filter(id__in=members).count()

        return Response(
            {
                "result": True,
                "data": {
                    "teams": {
                        "team_id": team.id,
                        "team_name": team.name,
                        "team_leader": team.admin.username,
                        "leader_id": team.admin.id,
                        "is_booking": team.is_booking,
                        "members": members,
                        "number_of_users": number_of_users
                    }
                }
            },
            status=status.HTTP_201_CREATED
        )


class AddTeamView(GenericAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = ()
    serializer_class = TeamCreateSerializer

    def post(self, request):
        # is_agency_admin = Agency.objects.filter(admin=request.user).exists()
        # is_permission = is_agency_admin | request.user.is_superuser
        # if not is_permission:
        #     return Response(
        #         {
        #             "result": False,
        #             "errorCode": 3,
        #             "errorMsg": "You don't have the permission."
        #         },
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = Team()
        team.name = serializer.data.get('team_name')
        team.admin = serializer.validated_data['admin']
        team.is_booking = serializer.validated_data['is_booking']
        team.save()
        members = serializer.data.get('members')
        if members:
            User.objects.filter(id__in=members).update(team=team, is_agent=False)
        return Response(
            {
                "result": True,
                "data": {
                    "msg": "Team created successfully."
                }
            },
            status=status.HTTP_201_CREATED
        )


class AllAgencyView(GenericAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = ()

    def get(self, request):
        # is_superuser = request.user.is_superuser
        # if not is_superuser:
        #     return Response(
        #         {
        #             "result": False,
        #             "errorCode": 3,
        #             "errorMsg": "You don't have the permission."
        #         },
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )
        keyword = request.GET.get('keyword')
        page = request.GET.get('page')
        number_per_page = request.GET.get('per_page')
        if keyword:
            allagencies = Agency.objects.filter(name__icontains=keyword).order_by('-id')
            number_of_agency = Agency.objects.filter(name__icontains=keyword).count()
        else:
            allagencies = Agency.objects.all().order_by('-id')
            number_of_agency = Agency.objects.all().count()
        paginator = Paginator(allagencies, number_per_page)
        try:
            search = paginator.page(page)
        except PageNotAnInteger:
            search = paginator.page(1)
        except EmptyPage:
            search = []

        sea_agency = []
        for sea in search:
            teams = Team.objects.filter(agency=sea)
            number_of_users = 0
            data_source = DataSource.objects.filter(agency=sea)
            data = []
            for item in data_source:
                data.append({
                    "id": item.id,
                    "pcc": item.pcc,
                    "provider": item.provider
                })
            for team in teams:
                number_of_users = number_of_users + User.objects.filter(team=team).count()
            sea_agency.append({
                **serialize_agency(sea),
                "number_of_users": number_of_users,
                "api_username": sea.api_username,
                "api_password": sea.api_password,
                "data_source": data
            })

        return Response(
            {
                "result": True,
                "data": {
                    "superuser_name": request.user.username,
                    "number_of_agencies": number_of_agency,
                    "agency": sea_agency
                }
            }
        )


class AgencyListView(GenericAPIView):

    def get(self, request):
        agency_list = Agency.objects.all()
        agency_detail = []
        for agency in agency_list:
            agency_detail.append({
                **serialize_agency(agency)
            })
        return Response(
            {
                "result": True,
                "data": {
                    "agency": agency_detail
                }
            },
            status=status.HTTP_201_CREATED
        )


class AddAgencyView(GenericAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = ()
    serializer_class = AgencyAddSerializer

    def post(self, request):
        # is_superuser = request.user.is_superuser
        # if not is_superuser:
        #     return Response(
        #         {
        #             "result": False,
        #             "errorCode": 3,
        #             "errorMsg": "You don't have the permission."
        #         },
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        agency = Agency()
        agency.name = serializer.data.get('agency_name')
        agency.api_username = serializer.data.get('api_username')
        agency.api_password = serializer.data.get('api_password')
        agency.save()
        data_source = serializer.data.get('data_source')
        if data_source:
            for data in data_source:
                try:
                    data_item = DataSource.objects.get(id=data['id'])
                    data_item.pcc = data['pcc']
                    data_item.agency = agency
                    data_item.save()
                except ObjectDoesNotExist:
                    return Response(
                        {
                            "result": False,
                            "data": {
                                "msg": "data_source is invalid."
                            }
                        },
                        status=status.HTTP_201_CREATED
                    )

        return Response(
            {
                "result": True,
                "data": {
                    "agency": {
                        "agency_id": agency.id,
                        "agency_name": agency.name,
                        "status": True,
                        "number_of_users": 0,
                        "api_username": agency.api_username,
                        "api_password": agency.api_password,
                        "data_source": data_source
                    }
                }
            },
            status=status.HTTP_201_CREATED
        )


class AgencyDetailView(GenericAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = ()
    serializer_class = AgencySerializer

    def get(self, request, pk):
        serializer = self.get_serializer(data={"agency_id": pk})
        serializer.is_valid(raise_exception=True)
        agency = serializer.validated_data['agency']
        data_array = DataSource.objects.filter(agency=agency)
        data_source = []
        for data in data_array:
            data_source.append({
                "id": data.id,
                "supplier": data.provider,
                "pcc": data.pcc
            })

        return Response(
            {
                "result": True,
                "data": {
                    "agency_id": agency.id,
                    "agency_name": agency.name,
                    "agency_api_username": agency.api_username,
                    "agency_api_password": agency.api_password,
                    "data_source": data_source
                }
            }
        )

    def delete(self, request, pk):
        try:
            is_agency_admin = Agency.objects.filter(admin=request.user).exists()
            is_permission = is_agency_admin | request.user.is_superuser
            if not is_permission:
                return Response(
                    {
                        "result": False,
                        "errorCode": 3,
                        "errorMsg": "You don't have the permission."
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            Team(id=pk).delete()

            return Response(
                {
                    "result": True,
                    "data": {
                        "msg": "Team removed successfully."
                    }
                }
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "result": False,
                    "errorCode": 1,
                    "errorMsg": "Invalid team id."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AgencyUpdateView(GenericAPIView):
    serializer_class = AgencyUpdateSerializer

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        agency = serializer.validated_data['agency']
        agency.name = serializer.data.get('agency_name')
        agency.api_username = serializer.data.get('api_username')
        agency.api_password = serializer.data.get('api_password')
        agency.save()
        data_source = serializer.data.get('data_source')
        DataSource.objects.filter(agency=agency).update(agency=None)
        if data_source:
            for data in data_source:
                try:
                    data_item = DataSource.objects.get(id=data['id'])
                    data_item.pcc = data['pcc']
                    data_item.agency = agency
                    data_item.save()
                except ObjectDoesNotExist:
                    return Response(
                        {
                            "result": False,
                            "data": {
                                "msg": "data_source is invalid."
                            }
                        },
                        status=status.HTTP_201_CREATED
                    )

        return Response(
            {
                "result": True,
                "data": {
                    "agency": {
                        "agency_id": agency.id,
                        "agency_name": agency.name,
                        "status": True,
                        "number_of_users": 0,
                        "api_username": agency.api_username,
                        "api_password": agency.api_password,
                        "data_source": data_source
                    }
                }
            },
            status=status.HTTP_201_CREATED
        )


class TeamAchieveView(GenericAPIView):

    def get(self, request, pk):
        try:
            user = Team.objects.get(id=pk)
            if user.is_booking:
                user.is_booking = False
            else:
                user.is_booking = True
            return Response(
                {
                    "result": True,
                    "data": {
                        "msg": "Team archived."
                    },
                },
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "result": False,
                    "data": {
                        "msg": "Team archive failed."
                    },
                },
            )


class DataSourceView(GenericAPIView):

    def get(self, request):
        data_source = DataSource.objects.filter(agency=None)
        data_source_detail = []
        for data in data_source:
            data_source_detail.append({
                "id": data.id,
                "provider": data.provider,
                "pcc": data.pcc
            })
        return Response(
            {
                "result": True,
                "data": {
                    "data_source": data_source_detail
                }
            },
            status=status.HTTP_201_CREATED
        )


class AvailableDataSourceView(GenericAPIView):

    def get(self, request, pk):
        agency = Agency.objects.get(id=pk)
        data_list = DataSource.objects.filter(Q(agency=agency) | Q(agency=None))
        data_detail = []
        for item in data_list:
            data_detail.append({
                "id": item.id,
                "pcc": item.pcc,
                "provider": item.provider
            })
        return Response(
            {
                "result": True,
                "data": {
                    "data_source": data_detail
                }
            },
            status=status.HTTP_201_CREATED
        )
