class User:
    def __init__(self, websocket, username):
        self.websocket = websocket
        self.username = username

    def get_websocket(self):
        return self.websocket

    def get_username(self):
        return self.username
