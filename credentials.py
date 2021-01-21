class Credentials:

    def __init__(self, username, password, host):
        if not username:
            raise Exception("No username provided")
        self._username = username

        if not password:
            raise Exception("No password provided")
        self._password = password

        if not host:
            raise Exception("No host provided")
        self._host = host

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        self._host = host

    @staticmethod
    def from_env() -> object:
        raise NotImplementedError
        return Credentials(None, None, None)

    @staticmethod
    def from_json(json_dict: dict):
        if not json_dict.get('username', False):
            raise Exception("No username provided")
        if not json_dict.get('password', False):
            raise Exception("No password provided")
        if not json_dict.get('host', False):
            raise Exception("No host provided")
        return Credentials(
            json_dict.get('username'),
            json_dict.get('password'),
            json_dict.get('host')
        )