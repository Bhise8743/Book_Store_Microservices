from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',extra='ignore')
    user_database_name: str
    postgresSQL_password: int
    secret_key: str
    jwt_algo: str
    redis_url: str
    email_sender: str
    email_password: str
    super_key: str


setting = Settings()
