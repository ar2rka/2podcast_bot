from pydantic import BaseSettings, Field


class Config(BaseSettings):
    BOT_ACCESS_KEY: str = Field(env='BOT_ACCESS_KEY')
    KAFKA_DSN: str = Field('localhost:9092', env='KAFKA_DSN')  # TODO: use pydantic.KafkaDsn
