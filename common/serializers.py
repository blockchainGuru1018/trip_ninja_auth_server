from rest_framework.permissions import IsAdminUser


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsAgencyAdmin(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_agency_admin or request.user.is_superuser)


class IsTeamLead(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_team_lead or request.user.is_agency_admin or request.user.is_superuser)


def serialize_user(user):
    return {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "last_login": user.last_login
    }


def serialize_team(team):
    return {
        "team_id": team.id,
        "team_name": team.name,
        "team_leader": team.admin.username
    }


def serialize_agency(agency):
    return {
        "agency_id": agency.id,
        "agency_name": agency.name,
        "status": agency.is_active
    }
