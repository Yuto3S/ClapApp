import secrets


class Room:
    def __init__(self):
        self.emitter_key = secrets.token_urlsafe(12)
        self.receiver_key = secrets.token_urlsafe(12)
        self.emitters = {}
        self.receivers = {}

    def add_emitter(self, emitter_key, user):
        if self.emitter_key != emitter_key:
            raise PermissionError

        self.emitters[user.get_id()] = user

    def remove_emitter(self, user):
        del self.emitters[user.get_id()]

    def add_receiver(self, receiver_key, user):
        if self.receiver_key != receiver_key:
            raise PermissionError
        if len(self.emitters) == 0:
            raise PermissionError

        self.receivers[user.get_id()] = user

    def remove_receiver(self, user):
        del self.receivers[user.get_id()]

    def get_all_users(self):
        return self.emitters | self.receivers

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
