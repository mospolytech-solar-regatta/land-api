from pydantic import BaseSettings


class PostgresConfig(BaseSettings):
    db: str
    password: str = 'postgres'
    server: str = '127.0.0.1'
    user: str  = 'postgres'
    port: int = '5433'

    class Config:
        env_prefix = 'postgres_'
        env_file = ".env"


class RedisConfig(BaseSettings):
    dsn: str = 'redis://localhost/'
    telemetry_channel: str = 'telemetry'

    class Config:
        env_prefix = 'redis_'
        env_file = ".env"
