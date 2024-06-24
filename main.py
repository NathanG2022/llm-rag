# from functools import wraps
import os

import uvicorn
from fastapi import FastAPI
from fastapi import status, Request
from starlette.responses import JSONResponse

from config import SETTINGS
from story import story_controller

app = FastAPI()
# app.include_router(rag_controller.router)
app.include_router(story_controller.router)


@app.get("/")
async def root():
    return {'app': SETTINGS.app_name}


# @lru_cache
# def get_settings():
#     return SETTINGS

# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# if os.getenv("PY_ENV", "local") != 'local':
#     @app.middleware("allow_internal_only")
#     async def allow_internal_only(request: Request, call_next):
#         appId: str = request.headers.get('X-Appengine-Inbound-Appid')
#         if not appId or appId not in SETTINGS.app_white_list:
#             return JSONResponse({"message": f"Access denied, {appId} not in whitelist."},
#                                 status_code=status.HTTP_403_FORBIDDEN)
#
#         response = await call_next(request)
#         return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8081, reload=True)
