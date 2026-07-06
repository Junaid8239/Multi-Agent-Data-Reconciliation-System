import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

params = urllib.parse.quote_plus(
    f"DRIVER={{{settings.sql_server_driver}}};"
    f"SERVER={settings.sql_server_host},{settings.sql_server_port};"
    f"DATABASE={settings.sql_server_db};"
    f"UID={settings.sql_server_user};"
    f"PWD={settings.sql_server_password};"
    f"TrustServerCertificate=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}", pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()