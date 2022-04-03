import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import Optional

from pydantic import BaseModel

from channel.base import BaseChannel
from utils.config import channels
from utils.email_template import EmailTemplate
from utils.pack import Pack


class Mail(BaseChannel):
    class Body(BaseModel):
        mail: str
        subject: Optional[str] = '中央通知'
        appellation: Optional[str] = '你好：'
        content: str

    sender = channels.mail.sender
    token = channels.mail.token
    smtp = channels.mail.smtp
    port = channels.mail.port

    @classmethod
    def handler(cls, body: Body, user):
        email = EmailTemplate(
            body.subject,
            '你好，{}：'.format(body.appellation),
            body.content,
        )

        msg = MIMEText(email.export(), 'html', 'utf-8')
        msg['From'] = formataddr(("中央通知服务", cls.sender))
        msg['To'] = formataddr((body.appellation, body.mail))
        msg['Subject'] = '【{}】通知'.format(user.name)

        try:
            server = smtplib.SMTP_SSL(cls.smtp, cls.port)
            server.login(cls.sender, cls.token)
            server.sendmail(cls.sender, [body.mail, ], msg.as_string())
            server.quit()
        except Exception:
            return Pack.error(msg='Mail Request')
        return Pack.ok()
