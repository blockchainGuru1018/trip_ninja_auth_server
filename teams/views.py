from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from teams.models import Team, Agency
from users.models import User
from .serializers import TeamAddSerializer, TeamUpdateSerializer


class AllTeamsView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        is_agency_admin = Agency.objects.filter(admin=request.user).exists()
        if not is_agency_admin:
            return Response(
                {
                    "result": False,
                    "errorCode": 3,
                    "errorMsg": "You don't have the permission."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        agency = Agency.objects.get(admin=request.user)
        number_of_teams = Team.objects.filter(agency=agency).count()
        team_list = Team.objects.filter(agency=agency)
        team_detail = []
        for team in team_list:
            number_of_teammembers = User.objects.filter(team=team).count()
            team_detail.append({
                "team_name": team.name,
                "team_admin": team.admin.username,
                "creatd_at": team.created_at,
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


class TeamDetailView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request, pk):
        try:
            team = Team.objects.get(id=pk)
            is_team_admin = Team.objects.filter(admin=request.user).exists()
            if not is_team_admin:
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
                    "is_active": agent.is_active,
                    "created_at": agent.created_at,
                    "updated_at": agent.updated_at
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
            if not is_agency_admin:
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


class AddTeamView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = TeamAddSerializer

    def post(self, request):
        is_agency_admin = Agency.objects.filter(admin=request.user).exists()
        if not is_agency_admin:
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
                    "Msg": "Team created",
                    "team_id": team.id,
                    "team_name": team.name,
                    "team_admin": team.admin.username,
                    "team_agency": team.agency.name
                }
            },
            status=status.HTTP_201_CREATED
        )


class UpdateTeamView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    serializer_class = TeamUpdateSerializer

    def put(self, request):
        is_agency_admin = Agency.objects.filter(admin=request.user).exists()
        if not is_agency_admin:
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
        team = serializer.validated_data['team']
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
