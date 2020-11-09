from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from teams.models import Team, Agency
from users.models import User
from .serializers import TeamSerializer, AgencySerializer


class AllTeamsView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
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
        if is_agency_admin:
            agency = Agency.objects.get(admin=request.user)
            number_of_teams = Team.objects.filter(agency=agency).count()
            team_list = Team.objects.filter(agency=agency)
            team_detail = []
            for team in team_list:
                number_of_teammembers = User.objects.filter(team=team).count()
                team_detail.append({
                    "team_name": team.name,
                    "team_admin": team.admin.username,
                    "created_at": team.created_at,
                    "number_of_teammembers": number_of_teammembers
                })

            return Response(
                {
                    "result": True,
                    "data": {
                        "Agency_name": agency.name,
                        "created_at": agency.created_at,
                        "admin_name": agency.admin.username,
                        "number_of_teams": number_of_teams,
                        "Team_details": team_detail
                    }
                }
            )
        else:
            number_of_teams = Team.objects.all().count()
            team_list = Team.objects.all()
            team_detail = []
            for team in team_list:
                number_of_teammembers = User.objects.filter(team=team).count()
                team_detail.append({
                    "team_name": team.name,
                    "team_admin": team.admin.username,
                    "created_at": team.created_at,
                    "number_of_teammembers": number_of_teammembers
                })

            return Response(
                {
                    "result": True,
                    "data": {
                        "number_of_teams": number_of_teams,
                        "Team_details": team_detail
                    }
                }
            )


class TeamDetailView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request, pk):
        try:
            team = Team.objects.get(id=pk)
            is_team_admin = Team.objects.filter(admin=request.user).exists()
            is_permission = is_team_admin | request.user.is_superuser
            if not is_permission:
                return Response(
                    {
                        "result": False,
                        "errorCode": 3,
                        "errorMsg": "You don't have the permission."
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            number_of_members = User.objects.filter(team=team).count()
            agent_list = User.objects.filter(team=team)
            agent_detail = []
            for agent in agent_list:
                agent_detail.append({
                    "email": agent.email,
                    "first_name": agent.first_name,
                    "last_name": agent.last_name,
                    "is_active": agent.is_active
                })

            return Response(
                {
                    "result": True,
                    "data": {
                        "team_name": team.name,
                        "created_at": team.created_at,
                        "admin_name": team.admin.username,
                        "number_of_agents": number_of_members,
                        "agent_details": agent_detail
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


class TeamEditView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = TeamSerializer

    def post(self, request):
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team = Team()
        team.name = serializer.data.get('name')
        team.agency = serializer.validated_data['agency']
        team.admin = serializer.validated_data['admin']
        team.common_parameters = serializer.validated_data['common_parameter']
        team.save()

        return Response(
            {
                "result": True,
                "data": {
                    "team_id": team.id,
                    "team_name": team.name,
                    "team_admin": team.admin.username,
                    "team_agency": team.agency.name
                }
            },
            status=status.HTTP_201_CREATED
        )

    def put(self, request, pk):
        try:
            team = Team.objects.get(id=pk)

            is_agency_admin = Agency.objects.filter(admin=request.user) == team.agency
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
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            team.name = serializer.data.get('name')
            team.agency = serializer.validated_data['agency']
            team.admin = serializer.validated_data['admin']
            team.common_parameters = serializer.validated_data['common_parameter']
            team.save()

            return Response(
                {
                    "result": True,
                    "data": {
                        "Msg": "Team updated",
                        "team_id": team.id,
                        "team_name": team.name,
                        "team_admin": team.admin.username,
                        "team_agency": team.agency.name
                    }
                },
                status=status.HTTP_201_CREATED
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "result": False,
                    "errorCode": 3,
                    "errorMsg": "team_id is invalid."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AgencyListView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        is_superuser = request.user.is_superuser
        if not is_superuser:
            return Response(
                {
                    "result": False,
                    "errorCode": 3,
                    "errorMsg": "You don't have the permission."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        number_of_agencies = Agency.objects.all().count()
        agency_list = Agency.objects.all()
        agency_detail = []
        for agency in agency_list:
            number_of_teams = Team.objects.filter(agency=agency).count()
            agency_detail.append({
                "agency_name": agency.name,
                "agency_admin": agency.admin.username,
                "created_at": agency.created_at,
                "number_of_teams": number_of_teams
            })

        return Response(
            {
                "result": True,
                "data": {
                    "superuser_name": request.user.username,
                    "number_of_agencies": number_of_agencies,
                    "agency_list": agency_detail
                }
            }
        )


class AgencyView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = AgencySerializer

    def post(self, request):
        is_superuser = request.user.is_superuser
        if not is_superuser:
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
        agency = Agency()
        agency.name = serializer.data.get('name')
        agency.amadeus_branded_fares = serializer.data.get('amadeus_branded_fares')
        agency.api_username = serializer.data.get('api_username')
        agency.api_password = serializer.data.get('api_password')
        agency.style_group = serializer.data.get('style_group')
        agency.is_iframe = serializer.data.get('is_iframe')
        agency.student_and_youth = serializer.data.get('student_and_youth')
        agency.common_parameters = serializer.validated_data['common_parameter']
        agency.admin = serializer.validated_data['admin']
        agency.save()

        return Response(
            {
                "result": True,
                "data": {
                    "agency_id": agency.id,
                    "agency_name": agency.name,
                    "agency_admin": agency.admin.username
                }
            },
            status=status.HTTP_201_CREATED
        )

    def put(self, request, pk):
        try:
            agency = Agency.objects.get(id=pk)
            is_permission = request.user.is_superuser | Agency.objects.get(admin=request.user)
            if not is_permission:
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
            agency.name = serializer.data.get('name')
            agency.amadeus_branded_fares = serializer.data.get('amadeus_branded_fares')
            agency.api_username = serializer.data.get('api_username')
            agency.api_password = serializer.data.get('api_password')
            agency.style_group = serializer.data.get('style_group')
            agency.is_iframe = serializer.data.get('is_iframe')
            agency.student_and_youth = serializer.data.get('student_and_youth')
            agency.common_parameters = serializer.validated_data['common_parameter']
            agency.admin = serializer.validated_data['admin']
            agency.save()

            return Response(
                {
                    "result": True,
                    "data": {
                        "agency_id": agency.id,
                        "agency_name": agency.name,
                        "agency_admin": agency.admin.username
                    }
                },
                status=status.HTTP_201_CREATED
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "result": False,
                    "errorCode": 3,
                    "errorMsg": "agency_id is invalid."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
