from flask_sqlalchemy import SQLAlchemy

# Instancia única de SQLAlchemy para toda la aplicación
db = SQLAlchemy()

def init_db(app):
    """Inicializa la base de datos con la aplicación Flask"""
    db.init_app(app)
    
    with app.app_context():
        # Crear todas las tablas si no existen
        try:
            db.create_all()
            print("Base de datos inicializada correctamente")
        except Exception as e:
            print(f"Error al inicializar la base de datos: {e}")

def get_db_session():
    """Retorna la sesión de la base de datos"""
    return db.session