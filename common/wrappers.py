from functools import wraps

from fastapi import HTTPException, status, Header

from config import SETTINGS


def check_inbound_appid(x_appengine_inbound_appid: str = Header(None)):
    if not x_appengine_inbound_appid or x_appengine_inbound_appid not in SETTINGS.app_white_list:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied, App ID not in whitelist.",
        )


# can only use on app controller, router controller doesn't work?
def internal(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        check_inbound_appid()
        return await func(*args, **kwargs)

    return wrapper
