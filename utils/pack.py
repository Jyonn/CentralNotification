class Pack:
    @staticmethod
    def base_response(ok: bool = True, body: dict = None, msg: str = None):
        return dict(
            ok=ok,
            msg=msg,
            body=body
        )

    @classmethod
    def ok(cls, body: dict = None):
        return cls.base_response(body=body)

    @classmethod
    def error(cls, msg: str = None):
        return cls.base_response(ok=False, msg=msg)
