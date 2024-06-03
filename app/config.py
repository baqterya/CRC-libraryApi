from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    app_port: str
    postgres_user: str
    postgres_password: str
    postgres_port: str
    postgres_db: str

    model_config = SettingsConfigDict(env_file="../.env")

    def get_url(self):
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@host.docker.internal:{self.postgres_port}/{self.postgres_db}"

