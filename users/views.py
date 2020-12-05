from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import GenericAPIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from teams.models import Team, Agency
from users.models import User
from common.serializers import serialize_user
from .serializers import GetUserByIdSerializer, SingleAddUserSerializer, BulkAddUserSerializer, UserUpdateSerializer


class UserDetailView(GenericAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = ()
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
    # authentication_classes = (TokenAuthentication,)

    def get(self, request):
        keyword = request.GET.get('keyword')
        page = request.GET.get('page')
        number_per_page = request.GET.get('per_page')
        sort_by = request.GET.get('sort_by')
        sort_order = request.GET.get('sort_order')
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

        sea_users = []
        for sea in search:
            if sea.team is None:
                team_name = None
                team_id = None
            else:
                team_name = sea.team.name
                team_id = sea.team.id
            sea_users.append({
                **serialize_user(sea),
                "email": sea.email,
                "phone_number": sea.phone_number,
                "team_id": team_id,
                "team_name": team_name,
                "is_active": sea.is_active,
                "role": "Team Lead"
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
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = ()
    serializer_class = SingleAddUserSerializer

    def post(self, request):
        # is_possible = Agency.objects.filter(admin=request.user) | Team.objects.filter(admin=request.user) | \
        #               request.user.is_superuser
        # if not is_possible:
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
        user = User()
        user.email = serializer.data.get('email')
        user.username = serializer.data.get('first_name') + " " + serializer.data.get('last_name')
        user.first_name = serializer.data.get('first_name')
        user.last_name = serializer.data.get('last_name')
        if serializer.validated_data['team']:
            user.team = serializer.validated_data['team']
        user.is_active = serializer.data.get('is_active')
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


class BulkAddUserView(GenericAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = ()
    serializer_class = BulkAddUserSerializer

    def post(self, request):
        # is_possible = Agency.objects.filter(admin=request.user) | Team.objects.filter(admin=request.user) | \
        #               request.user.is_superuser
        # if not is_possible:
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
        emails = serializer.data.get('emails')
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
                        user.is_active = serializer.data.get('is_active')
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
                    user.is_agent = True
                    user.is_active = serializer.data.get('is_active')
                    user.save()

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
        team_id = team_name = None
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.username = serializer.data.get('username')
        user.email = serializer.data.get('email')
        if serializer.data.get('phone_number'):
            user.phone_number = serializer.data.get('phone_number')
        user.is_active = serializer.data.get('is_active')
        if serializer.data.get('team_id'):
            user.team = Team.objects.get(id=serializer.data.get('team_id'))
            team_id = user.team.id
            team_name = user.team.name
        user.save()
        if not user.team:
            team_id = None
            team_name = None

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
                        "role": "Team Lead"
                    }
                }
            },
            status=status.HTTP_201_CREATED
        )


class UserAchieveView(GenericAPIView):

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            if user.is_active:
                user.is_active = False
            else:
                user.is_active = True
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
