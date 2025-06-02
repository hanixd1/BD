from flask import Flask, render_template
from database import db
from models.paciente import Paciente
from models.medico import Medico
from models.cita import Cita
from models.historial import Historial

app = Flask(__name__)

# Configura tu conexión a SQL Server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:TuContraseña@DESKTOP-NPKC1CP/TuBaseDeDatos?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base de datos
db.init_app(app)

# Crea las tablas si no existen
with app.app_context():
    db.create_all()

# Ruta para mostrar la página principal y pacientes
@app.route('/')
def pagina_inicio():
    return render_template('pagina1.html')

if __name__ == '__main__':
    app.run(debug=True)