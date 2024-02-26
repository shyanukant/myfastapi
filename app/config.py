from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    host: str 
    user: str 
    password: str 
    database: str 
    
    secret_key: str 
    algorithm: str
    access_token_expire_minutes: int = 30

    class Config:
        env_file = '.env'

settings = Settings()