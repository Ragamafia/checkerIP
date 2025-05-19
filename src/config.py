from pydantic_settings import BaseSettings


DEFAULT_PROXY = ""

class Config(BaseSettings):
    class Config:
        extra='ignore'
        env_file = '../env/.env'
        env_file_encoding = 'utf-8'

    ## Main
    proxy: str = DEFAULT_PROXY


cfg = Config()
