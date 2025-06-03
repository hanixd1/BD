from datetime import datetime, time
from database import db

class Cita(db.Model):
    __tablename__ = 'Cita'
    
    id_cita = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dni_paciente = db.Column(db.String(8), db.ForeignKey('Paciente.DNI'), nullable=False)
    id_medico = db.Column(db.String(10), db.ForeignKey('Medico.id_medico'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    motivo = db.Column(db.String(200), nullable=False)
    prioridad = db.Column(db.String(10), nullable=False)  # Ajustado a 10 caracteres
    estado = db.Column(db.String(15), nullable=False, default='Programada')
    modalidad = db.Column(db.String(15), nullable=False)
    nivel_molestia = db.Column(db.String(15))
    persistencia = db.Column(db.String(15))
    notas = db.Column(db.String(500))
    ultima_visita = db.Column(db.Date)
    intervencion = db.Column(db.String(20))
    
    # Relaciones ORM
    paciente = db.relationship('Paciente', back_populates='citas')
    medico = db.relationship('Medico', back_populates='citas')
    
    def __repr__(self):
        return f'<Cita {self.id_cita} - {self.fecha} {self.hora}>'