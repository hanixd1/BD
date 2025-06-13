from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import db
from models.paciente import Paciente
from models.medico import Medico
from models.cita import Cita
from models.historial import Historial

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para usar sesiones y flash messages

# Configura tu conexión a SQL Server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:147852@DESKTOP-NPKC1CP/GestorSaludRural?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base de datos
db.init_app(app)

# Ruta para mostrar la página principal
@app.route('/')
def pagina_inicio():
    return render_template('pagina1.html')

# Ruta para página2
@app.route('/pagina2')
def pagina2():
    return render_template('pagina2.html')

# Ruta para página3
@app.route('/pagina3')
def pagina3():
    return render_template('pagina3.html')

# Ruta para procesar el formulario de cita (página1 -> página2)
@app.route('/procesar_cita', methods=['POST'])
def procesar_cita():
    if request.method == 'POST':
        # Obtener los datos del formulario
        dni = request.form.get('DNI')
        codigo = request.form.get('PC_NOMBRE')
        apellido = request.form.get('PC_APELLIDO')
        fechanac = request.form.get('PC_FECHA_NACIMIENTO')
        tutor = request.form.get('TUTOR_APODERADO')
        motivo = request.form.get('motivo')
        sexo = request.form.get('sexo')
        edad = request.form.get('edad')
        modalidad = request.form.get('modalidad')
        seguro = request.form.get('seguro')
        fecha = request.form.get('fecha')
        
        # Guardar datos en sesión para usar en las siguientes páginas
        session['datos_cita'] = {
            'dni': dni,
            'codigo': codigo,
            'apellido': apellido,
            'fechanac': fechanac,
            'tutor': tutor,
            'motivo': motivo,
            'sexo': sexo,
            'edad': edad,
            'modalidad': modalidad,
            'seguro': seguro,
            'fecha': fecha
        }
        
        # Redirige a página2 después de procesar
        return redirect(url_for('pagina2'))

# Ruta para procesar el formulario de descripción médica (página2 -> página3)
@app.route('/procesar_descripcion', methods=['POST'])
def procesar_descripcion():
    if request.method == 'POST':
        # Obtener datos del formulario de página2
        condicion_medica = request.form.get('condicionMedica')
        descripcion = request.form.get('descripcion')
        gravedad = request.form.get('gravedad')
        molestia = request.form.get('molestia')
        persistencia = request.form.get('persistencia')
        fecha_visita = request.form.get('fechaVisita')
        tiene_visita_previa = request.form.get('tieneVisitaPrevia') == 'true'
        
        # Validar que los campos requeridos estén presentes
        if not condicion_medica or not descripcion:
            flash('Por favor complete todos los campos requeridos', 'error')
            return redirect(url_for('pagina2'))
        
        # Guardar datos de descripción médica en sesión
        session['datos_descripcion'] = {
            'condicion_medica': condicion_medica,
            'descripcion': descripcion,
            'gravedad': gravedad,
            'molestia': molestia,
            'persistencia': persistencia,
            'fecha_visita': fecha_visita,
            'tiene_visita_previa': tiene_visita_previa
        }
        
        # Redirigir a página3
        return redirect(url_for('pagina3'))

# Ruta para procesar la selección de médico (página3 -> finalizar)
@app.route('/procesar_medico', methods=['POST'])
def procesar_medico():
    if request.method == 'POST':
        # Obtener datos del formulario de página3
        medico_seleccionado = request.form.get('medico_seleccionado')
        fecha_seleccionada = request.form.get('fecha_seleccionada')
        hora = request.form.get('hora')
        minutos = request.form.get('minutos')
        especialidad_seleccionada = request.form.get('especialidad_seleccionada')
        
        # Validar campos requeridos
        if not medico_seleccionado or not fecha_seleccionada:
            flash('Por favor seleccione un médico y una fecha', 'error')
            return redirect(url_for('pagina3'))
        
        # Obtener todos los datos de las sesiones anteriores
        datos_cita = session.get('datos_cita', {})
        datos_descripcion = session.get('datos_descripcion', {})
        
        # Aquí puedes procesar y guardar toda la información en la base de datos
        try:
            # Ejemplo de cómo guardar los datos (ajusta según tus modelos)
            # nuevo_paciente = Paciente(...)
            # nueva_cita = Cita(...)
            # db.session.add(nuevo_paciente)
            # db.session.add(nueva_cita)
            # db.session.commit()
            
            # Limpiar sesión después de procesar
            session.pop('datos_cita', None)
            session.pop('datos_descripcion', None)
            
            flash('Cita agendada exitosamente', 'success')
            return redirect(url_for('pagina_inicio'))
            
        except Exception as e:
            flash(f'Error al procesar la cita: {str(e)}', 'error')
            return redirect(url_for('pagina3'))

# Ruta para cancelar y volver al inicio
@app.route('/cancelar')
def cancelar():
    # Limpiar sesión
    session.pop('datos_cita', None)
    session.pop('datos_descripcion', None)
    return redirect(url_for('pagina_inicio'))

# Ruta para retroceder a la página anterior
@app.route('/retroceder_a_pagina1')
def retroceder_a_pagina1():
    return redirect(url_for('pagina_inicio'))

@app.route('/retroceder_a_pagina2')
def retroceder_a_pagina2():
    return redirect(url_for('pagina2'))

# Ruta para manejar errores 404 (opcional)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)