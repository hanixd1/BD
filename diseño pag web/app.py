from flask import Flask, render_template, request, redirect, url_for
from database import db
from models.paciente import Paciente
from models.medico import Medico
from models.cita import Cita
from models.historial import Historial

app = Flask(__name__)

# Configura tu conexión a SQL Server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:TuContraseña@DESKTOP-NPKC1CP/GestorSaludRural?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base de datos
db.init_app(app)

# Ruta para mostrar la página principal y pacientes
@app.route('/')
def pagina_inicio():
    return render_template('pagina1/pagina1.html')

@app.route('/procesar_cita', methods=['POST'])
def procesar_cita():
    datos = request.form
    # Aquí puedes guardar los datos, validarlos o enviarlos a una BD
    print("Datos recibidos:", datos)  # Solo para probar
    return redirect(url_for('pagina_inicio'))  # Redirige después de procesar

@app.route('/cancelar')
def cancelar():
    return redirect(url_for('pagina_inicio'))  # Puedes hacer algo distinto si quieres

@app.route('/pagina2', methods=['POST'])
def pagina2():
    datos = request.form
    print("Datos de cita:", datos)
    return render_template('pagina2.html', datos=datos)

if __name__ == '__main__':
    app.run(debug=True)