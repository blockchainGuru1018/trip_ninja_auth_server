

def serialize_user(user):
    return {
        "user_id": user.id,
        "username": user.username,
        "last_login": user.last_login
    }
