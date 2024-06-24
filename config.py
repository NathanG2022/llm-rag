import os

from pydantic_settings import BaseSettings, SettingsConfigDict

from common.utils import getAbsPathLocatedFromCurFile

if os.getenv("PY_ENV", "local") == 'local':
    os.environ['https_proxy'] = 'http://127.0.0.1:7078'


class Settings(BaseSettings):
    app_name: str = "Customer Service - Q&A"
    openai_api_key: str
    redis_url: str
    env: str = os.getenv("PY_ENV", "local")
    app_white_list: list = [
        'portal-gateway-dev-dot-mobile-app-services',
        'portal-gateway-staging-dot-mobile-app-services',
        'portal-gateway-prod-dot-mobile-app-services',
    ]

    model_config = SettingsConfigDict(
        env_file=getAbsPathLocatedFromCurFile(__file__, "./config/.env." + os.getenv("PY_ENV", "local")))

    def __init__(self, *args, **kwargs):
        # if os.getenv("PY_ENV", "local") != 'prod':
        #     self.model_config = SettingsConfigDict(env_file="config/.env." + os.getenv("PY_ENV", "local"))
        super().__init__(*args, **kwargs)


SETTINGS = Settings()

if __name__ == "__main__":
    print(getAbsPathLocatedFromCurFile(__file__, './config/.env.'))
    print(os.path.curdir)
    print(SETTINGS.redis_url)

    # root_directory = os.path.dirname(os.path.dirname(script_path))
    #
    # print(root_directory)
