from pydantic_settings import BaseSettings


DEFAULT_PROXY = ""

class Config(BaseSettings):
    class Config:
        extra='ignore'
        env_file = "../env/.env"
        env_file_encoding = 'utf-8'

    ## Main
    dev: bool = False
    proxy: str = DEFAULT_PROXY
    proxy_check_timeout: int = 6
    proxy_scam_check_attempts: int = 1


cfg = Config()
