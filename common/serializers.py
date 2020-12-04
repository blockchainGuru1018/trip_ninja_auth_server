

def serialize_user(user):
    return {
        "user_id": user.id,
        "username": user.username,
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
        "status": agency.is_iframe
    }
