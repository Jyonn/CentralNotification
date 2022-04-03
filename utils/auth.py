from utils.config import users
from utils.md5 import MD5
from utils.pack import Pack


class Auth:
    @classmethod
    def validate(cls, auth: str):
        auth = auth.split('$', 1)
        if len(auth) != 2:
            raise Exception('Unpack Token')
        uid, token = auth

        if uid not in users.d:
            raise Exception('User Not Found')
        user = users.d[uid]
        if user.type == 'raw':
            if user.token == token:
                return user
        elif user.type == 'md5':
            if user.token == MD5.get(token):
                return user
        else:
            raise Exception('Encrypt Type Not Found')

        raise Exception('Authentication Failed')
