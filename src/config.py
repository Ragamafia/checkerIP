from pathlib import Path

from pydantic_settings import BaseSettings


DEFAULT_PROXY = ""

class Config(BaseSettings):
    class Config:
        extra='ignore'
        env_file = "../env/.env"
        env_file_encoding = 'utf-8'

    ## Main
    dev: bool = False
    sql_lite_db_path: Path = Path("../data/database.db")
    bot_token: str = ''
    proxy: str = DEFAULT_PROXY
    new_user_balance: int = 0
    need_approve: bool = False
    proxy_check_timeout: int = 6
    proxy_scam_check_attempts: int = 1
    api_key_ipquality: str = ''


cfg = Config()
