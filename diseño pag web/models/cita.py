from datetime import datetime, time
from database import db

class Cita(db.Model):
    __tablename__ = 'Cita'
    
    id_cita = db.Column(db.Integer, primary_key=True, name='ID_CITA')
    fecha = db.Column(db.Date, name='CT_FECHA_CITA')
    hora = db.Column(db.Time, name='CT_HORA_CITA')
    motivo = db.Column(db.String(200), name='CT_MOTIVO')
    prioridad = db.Column(db.String(50), name='CT_PRIORIDAD')
    estado = db.Column(db.String(50), name='CT_ESTADO')
    
    # Relaciones (claves foráneas)
    dni_paciente = db.Column(db.String(8), db.ForeignKey('Paciente.DNI'), name='DNI')
    id_medico = db.Column(db.String(10), db.ForeignKey('Medico.id_medico'), name='ID_MEDICO')
    id_historial = db.Column(db.Integer, db.ForeignKey('Historial.ID_HISTORIAL'), name='ID_HISTORIAL')
    
    # Relaciones ORM
    paciente = db.relationship('Paciente', back_populates='citas')
    medico = db.relationship('Medico', back_populates='citas')
    historial = db.relationship('Historial', back_populates='citas')
    
    def __repr__(self):
        return f'<Cita {self.id_cita} - {self.fecha} {self.hora}>'