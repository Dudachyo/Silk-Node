from pydantic_settings import BaseSettings , SettingsConfigDict


class Settings(BaseSettings):
    """
        settings for database
    """
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    """
        settings for security
    """

    JWT_ACCESS_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
    REFRESH_TOKEN_EXPIRE_DAY: int = 7



    @property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()

