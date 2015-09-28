import email.mime.text
import uuid
import multiprocessing.pool

import settings


class User(object):
    collection = settings.db['users']

    def __init__(self, login, **kwargs):
        self.id = kwargs.get('_id')
        self.login = login
        self.data = kwargs.get('data')
        self.token = kwargs.get('token', str(uuid.uuid4()))
        self.gh_token = kwargs.get('gh_token')

    def __lt__(self, other):
        return self.login < other.login

    @property
    def name(self):
        if self.data and self.data.get('name'):
            return self.data['name']
        else:
            return self.login

    @property
    def admin(self):
        return self.login in settings.ADMINS

    @classmethod
    def get(cls, token=None, login=None):
        query = {}
        if token:
            query['token'] = token
        if login:
            query['login'] = login

        if not query:
            return None

        user = User.collection.find_one(query)
        return cls(**user) if user else None

    def put(self):
        saved = self.id is not None
        user = {
            'login': self.login,
            'data': self.data,
            'token': self.token,
            'gh_token': self.gh_token,
        }

        if saved:
            user['_id'] = self.id

        self.id = User.collection.save(user)
