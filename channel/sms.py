from pydantic import BaseModel

from channel.base import BaseChannel
from utils.config import channels
from utils.grabber import Grabber
from utils.pack import Pack


class SMS(BaseChannel):
    class Body(BaseModel):
        phone: str
        content: str

    worker = Grabber(
        data_type='form',
        headers={
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        },
    )
    active = True
    apikey = channels.sms.apikey
    appurl = "https://sms.yunpian.com/v2/sms/single_send.json"
    template = '【MasterWhole】命令#name#的运行结果已出：#message#'

    @classmethod
    def handler(cls, body: Body, user):
        if not body.phone.startswith('+'):
            body.phone = '+86' + body.phone

        try:
            cls.worker.post(cls.appurl, data=dict(
                apikey=cls.apikey,
                text=cls.template.replace('#message#', body.content).replace('#name#', user.name),
                mobile=body.phone,
            ))
        except Exception:
            return Pack.error(msg='SMS Request')

        return Pack.ok()
