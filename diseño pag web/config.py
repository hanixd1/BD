import urllib

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-NPKC1CP;"
    "DATABASE=GestorSaludRural;"  # ← Cambia esto por el nombre real
    "UID=sa;"
    "PWD=147852"
)

SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
