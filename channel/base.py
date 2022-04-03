import abc

from pydantic import BaseModel

from utils.pack import Pack


class BaseChannel(abc.ABC):
    active = True

    @classmethod
    def handler(cls, body: BaseModel, user):
        raise NotImplementedError

    @classmethod
    def run(cls, body: BaseModel, user):
        if not cls.active:
            return Pack.error(msg='Channel inactive')
        return cls.handler(body, user)
