import secrets


class Room:
    def __init__(self):
        self.emitter_key = secrets.token_urlsafe(12)
        self.receiver_key = secrets.token_urlsafe(12)
        self.emitters = {}
        self.receivers = {}

    def add_user(self, user, emitter_key=None, receiver_key=None):
        if emitter_key:
            self.add_emitter(user=user, emitter_key=emitter_key)
        elif receiver_key:
            self.add_receiver(user=user, receiver_key=receiver_key)
        else:
            raise KeyError

    def add_emitter(self, emitter_key, user):
        if self.emitter_key != emitter_key:
            raise PermissionError

        self.emitters[user.get_id()] = user

    def add_receiver(self, receiver_key, user):
        if self.receiver_key != receiver_key:
            raise PermissionError
        if len(self.emitters) == 0:
            raise PermissionError

        self.receivers[user.get_id()] = user

    def remove_user(self, user, emitter_key=None, receiver_key=None):
        if emitter_key:
            self.remove_emitter(user=user)
        elif receiver_key:
            self.remove_receiver(user=user)
        else:
            raise KeyError

    def remove_receiver(self, user):
        del self.receivers[user.get_id()]

    def remove_emitter(self, user):
        del self.emitters[user.get_id()]

    def get_all_users(self):
        return self.emitters | self.receivers

    def get_all_users_websocket(self):
        return [user.get_websocket() for user in self.get_all_users().values()]

    def get_user(self, user_id):
        all_users = self.get_all_users()
        return all_users.get(user_id)

    def get_emitters(self):
        return self.emitters

    def get_receivers(self):
        return self.receivers

    def get_emitter_key(self):
        return self.emitter_key

    def get_receiver_key(self):
        return self.receiver_key
