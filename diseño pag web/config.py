import urllib.parse

# Configuración de la base de datos
SERVER = 'DESKTOP-NPKC1CP'  # Cambia por tu servidor real
DATABASE = 'GestorSaludRural'
USERNAME = 'sa'
PASSWORD = '147852'

# Parámetros de conexión
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    "TrustServerCertificate=yes;"
    "Encrypt=yes"
)

# URI de SQLAlchemy
SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuración adicional
SECRET_KEY = 'tu_clave_secreta_aqui_cambiala_por_una_mas_segura'