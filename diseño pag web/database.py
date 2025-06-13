from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Configuración de conexión (ajusta estos valores según tu imagen)
SERVER = 'DESKTOP-NPKCIGP' 
DATABASE = 'GestorSaludRural' 
USERNAME = 'sa'
PASSWORD = '147852'

# Cadena de conexión para SQL Server
SQLALCHEMY_DATABASE_URL = (
    f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&TrustServerCertificate=yes"  # Opción que tienes marcada en tu imagen
    "&encrypt=yes"  # Encryption: Mandatory
)

# Crear el motor de SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 15}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Función para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()