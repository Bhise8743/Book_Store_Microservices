from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',extra='ignore')
    book_database_name: str
    postgresSQL_password: int
    secret_key: str
    jwt_algo: str


setting = Settings()
