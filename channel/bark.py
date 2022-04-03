from typing import Optional
from urllib.parse import quote

from pydantic import BaseModel

from channel.base import BaseChannel
from utils.grabber import Grabber
from utils.pack import Pack


class Bark(BaseChannel):
    class Body(BaseModel):
        uri: str
        content: str
        title: Optional[str] = None
        sound: Optional[str] = None
        icon: Optional[str] = None
        group: Optional[str] = None
        url: Optional[str] = None

    worker = Grabber()
    active = True

    @classmethod
    def handler(cls, body: Body, user):
        if not body.uri.endswith('/'):
            body.uri += '/'

        if not body.title:
            body.title = ''
        body.title = '【{}】{}'.format(user.name, body.title)
        path = '%s%s/%s' % (body.uri, quote(body.title), quote(body.content))

        query = dict()
        params = ['sound', 'url', 'icon', 'group']
        for param in params:
            value = getattr(body, param)
            if value:
                query[param] = value

        try:
            cls.worker.get(path, query=query)
        except Exception:
            return Pack.error(msg='Bark Request')
        return Pack.ok()
