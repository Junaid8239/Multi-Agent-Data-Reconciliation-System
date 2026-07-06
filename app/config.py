from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str
    groq_model: str = "groq/llama-3.3-70b-versatile"

    sql_server_host: str
    sql_server_port: int = 1433
    sql_server_db: str
    sql_server_user: str
    sql_server_password: str
    sql_server_driver: str = "ODBC Driver 18 for SQL Server"

    class Config:
        env_file = ".env"

settings = Settings()