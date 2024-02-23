from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    host: str = 'localhost'
    port: int = 5432
    user: str = 'admin'
    password: str = 'LocalPasswordOnly'
    database: str = 'postgres'
    
    secret_key: str = 'djfkjeifjidkfdknnnmnv,mdlkfjekjiojikfndfojoirieeuriueijfkdnfkdsjjf'
    algorithm: str = 'HS256'
    access_token_expire_minutes: int = 30

    # class Config:
    #     env_file = '.env'

settings = Settings()