from fastapi import FastAPI, Header

from channel.bark import Bark
from channel.mail import Mail
from channel.sms import SMS
from utils.auth import Auth
from utils.pack import Pack

app = FastAPI()
channel_list = [Bark, Mail, SMS]


@app.get("/")
async def root():
    return list(map(lambda c: c.__name__, filter(lambda c: c.active, channel_list)))


@app.post("/bark")
async def bark(
        body: Bark.Body,
        auth=Header(...),
):
    try:
        user = Auth.validate(auth)
    except Exception as e:
        return Pack.error(msg=e.args[0])
    return Bark.run(body, user)


@app.post("/sms")
async def sms(
        body: SMS.Body,
        auth=Header(...),
):
    try:
        user = Auth.validate(auth)
    except Exception as e:
        return Pack.error(msg=e.args[0])
    return SMS.run(body, user)


@app.post("/mail")
async def mail(
        body: Mail.Body,
        auth=Header(...),
):
    try:
        user = Auth.validate(auth)
    except Exception as e:
        return Pack.error(msg=e.args[0])
    return Mail.run(body, user)
