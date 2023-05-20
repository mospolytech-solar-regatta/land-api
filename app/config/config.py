from pydantic import BaseSettings


class Config(BaseSettings):
    postgres_db: str
    postgres_password: str = 'postgres'
    postgres_server: str = '127.0.0.1'
    postgres_user: str = 'postgres'
    postgres_port: int = '5433'
    redis_dsn: str = 'redis://localhost/'
    redis_telemetry_channel: str = 'telemetry'
    allow_origin: str = '["*"]'
    origin: str = "http://localhost:8000"

    class Config:
        env_file = ".env"


