import secrets


class Room:
    def __init__(self):
        self.emitter_key = secrets.token_urlsafe(12)
        self.receiver_key = secrets.token_urlsafe(12)
        self.emitters = set()
        self.receivers = set()

    def add_emitter(self, emitter_key, user):
        if self.emitter_key != emitter_key:
            raise PermissionError

        self.emitters.add(user)

    def remove_emitter(self, user):
        self.emitters.remove(user)

    def add_receiver(self, receiver_key, user):
        if self.receiver_key != receiver_key:
            raise PermissionError
        if len(self.emitters) == 0:
            raise PermissionError

        self.receivers.add(user)

    def remove_receiver(self, user):
        self.receivers.remove(user)

    def get_emitters(self):
        return self.emitters

    def get_receivers(self):
        return self.receivers
