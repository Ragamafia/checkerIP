from pydantic_settings import BaseSettings


DEFAULT_PROXY = "http://e84fe8de4bf5d759b6dc:4756263bc8d0bb04@gw.dataimpulse.com:823"

class Config(BaseSettings):
    class Config:
        extra='ignore'
        env_file = '../env/.env'
        env_file_encoding = 'utf-8'

    ## Main
    proxy: str = DEFAULT_PROXY


cfg = Config()
