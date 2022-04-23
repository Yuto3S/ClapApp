class User:
    def __init__(self, websocket, username, id, picture=None):
        self.websocket = websocket
        self.username = username
        self.picture = picture
        self.id = id

    def get_websocket(self):
        return self.websocket

    def get_username(self):
        return self.username

    def get_id(self):
        return self.id

    def get_picture(self):
        return self.picture

    def update_picture(self, picture):
        self.picture = picture

    def update_name(self, username):
        self.username = username
