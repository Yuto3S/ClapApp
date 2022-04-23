UPDATE = "update"
DELETE = "delete"
ALL_USERS = "all_users"
SINGLE_USER = "single_user"
USER = "user"
ROOM = "room"


def get_all_users_event(all_users):
    return {
        "action": UPDATE,
        "update": ALL_USERS,
        "users": [
            get_single_user_format(all_users[user_id]) for user_id in all_users.keys()
        ],
    }


def get_single_user_update_event(user):
    return {
        "action": UPDATE,
        "update": SINGLE_USER,
        "user": get_single_user_format(user),
    }


def get_user_disconnected_event(user):
    return {
        "action": DELETE,
        "delete": USER,
        "user": get_single_user_format(user),
    }


def get_single_user_format(user):
    return {
        "name": user.get_username(),
        "id": user.get_id(),
        "picture": user.get_picture(),
    }


def get_room_closed_event():
    return {
        "action": DELETE,
        "delete": ROOM,
    }
