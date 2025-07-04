import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
import config
from database import db, init_db
from models.cita import Cita
from models.historialcita import HistorialCita
from models.medico import Medico  
from models.paciente import Paciente
from models.condicionmedica import CondicionMedica
from models.horariomedico import HorarioMedico

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()  # También mostrar en consola
    ]
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    # Configuración desde config.py
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = config.SECRET_KEY
    
    # Inicializar la base de datos
    init_db(app)
    
    return app

app = create_app()

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
        medico_seleccionado = request.form.get('medico_seleccionado')
        fecha_seleccionada = request.form.get('fecha_seleccionada')
        hora = request.form.get('hora')
        minutos = request.form.get('minutos')
        especialidad_seleccionada = request.form.get('especialidad_seleccionada')
        
        if not medico_seleccionado or not fecha_seleccionada:
            flash('Por favor seleccione un médico y una fecha', 'error')
            return redirect(url_for('pagina3'))
        
        # Obtener todos los datos de las sesiones anteriores
        datos_cita = session.get('datos_cita', {})
        datos_descripcion = session.get('datos_descripcion', {})
        
        try:
            # Primero verificar si el paciente existe, si no, crearlo
            paciente = Paciente.query.filter_by(DNI=datos_cita.get('dni')).first()
            if not paciente:
                paciente = Paciente(
                    DNI=datos_cita.get('dni'),
                    nombres=datos_cita.get('codigo'),
                    apellidos=datos_cita.get('apellido'),
                    sexo=datos_cita.get('sexo'),
                    edad=int(datos_cita.get('edad', 0)),
                    fecha_nacimiento=datos_cita.get('fechanac'),
                    tutor_apoderado=datos_cita.get('tutor'),
                    tipo_seguro=datos_cita.get('seguro')
                )
                db.session.add(paciente)
            
            # Crear la cita
            nueva_cita = Cita(
                dni_paciente=datos_cita.get('dni'),
                id_medico=medico_seleccionado,
                fecha=fecha_seleccionada,
                hora=f"{hora}:{minutos}:00",
                motivo=datos_cita.get('motivo'),
                modalidad=datos_cita.get('modalidad'),
                descripcion_condicion=datos_descripcion.get('descripcion'),
                gravedad=datos_descripcion.get('gravedad'),
                nivel_molestia=datos_descripcion.get('molestia'),
                persistencia=datos_descripcion.get('persistencia'),
                fecha_ultima_visita=datos_descripcion.get('fecha_visita'),
                tiene_visita_previa=datos_descripcion.get('tiene_visita_previa', False)
            )
            
            db.session.add(nueva_cita)
            db.session.commit()
            
            # Limpiar sesión después de procesar
            session.pop('datos_cita', None)
            session.pop('datos_descripcion', None)
            
            flash('Cita agendada exitosamente', 'success')
            return redirect(url_for('pagina_inicio'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al procesar la cita: {str(e)}', 'error')
            return redirect(url_for('pagina3'))

# Ruta para cancelar y volver al inicio
@app.route('/cancelar')
def cancelar():
    session.pop('datos_cita', None)
    session.pop('datos_descripcion', None)
    return redirect(url_for('pagina_inicio'))

# Rutas para retroceder
@app.route('/retroceder_a_pagina1')
def retroceder_a_pagina1():
    return redirect(url_for('pagina_inicio'))

@app.route('/retroceder_a_pagina2')
def retroceder_a_pagina2():
    return redirect(url_for('pagina2'))

# Ruta para obtener médicos por especialidad (AJAX)
@app.route('/api/medicos/<especialidad>')
def obtener_medicos(especialidad):
    medicos = Medico.query.filter_by(especialidad=especialidad, activo=True).all()
    return {
        'medicos': [
            {
                'id': medico.id_medico,
                'nombre': f"{medico.nombres} {medico.apellidos}"
            } for medico in medicos
        ]
    }

# Manejo de errores
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
#ruta para confirmar conexion
@app.route('/debug/bd_status')
def bd_status():
    """Ruta para verificar el estado de la base de datos"""
    try:
        # Contar registros
        total_pacientes = Paciente.query.count()
        total_medicos = Medico.query.count()
        total_citas = Cita.query.count()
        
        # Últimas citas
        ultimas_citas = Cita.query.order_by(Cita.fecha_creacion.desc()).limit(5).all()
        
        info = {
            'status': 'OK',
            'totales': {
                'pacientes': total_pacientes,
                'medicos': total_medicos,
                'citas': total_citas
            },
            'ultimas_citas': [
                {
                    'numero': cita.numero_cita,
                    'paciente_dni': cita.dni_paciente,
                    'fecha': str(cita.fecha),
                    'hora': str(cita.hora),
                    'creada': str(cita.fecha_creacion)
                } for cita in ultimas_citas
            ]
        }
        
        return info
        
    except Exception as e:
        return {
            'status': 'ERROR',
            'mensaje': str(e)
        }