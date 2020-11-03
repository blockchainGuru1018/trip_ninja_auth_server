

def serialize_user(user):
    return {
        "user_id": user.id,
        "username": user.username,
        "createdAt": user.date_joined,
        "updatedAt": user.date_joined
    }
