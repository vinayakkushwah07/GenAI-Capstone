from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "MyApp"  
    DATABASE_URL:str
    GROQ_API_KEY:str
    MODEL:str
    ADV_MODEL:str
    CHROMA_DB_PATH:str
    FILE_PATH:str
    CHROMA_COLLECTION_NAME:str
    CHROMA_COLLECTION_NAME:str
    EMBEDDING_MODEL:str
    secret_key: str
    refresh_secret_key : str
    algorithm: str
    timeout: int
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    REFRESH_TOKEN_EXPIRE_MINUTES : int
    model_config = SettingsConfigDict(extra='allow',env_file=".env")


settings = Settings()

