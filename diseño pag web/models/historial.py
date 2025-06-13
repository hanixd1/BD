from datetime import datetime
from database import db

class Historial(db.Model):
    __tablename__ = 'Historial'
    
    id_historial = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dni_paciente = db.Column(db.String(8), db.ForeignKey('Paciente.DNI'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, 
                                   onupdate=datetime.utcnow, nullable=False)
    diagnostico = db.Column(db.Text, nullable=False)
    tratamiento = db.Column(db.Text)
    medicamentos = db.Column(db.Text)
    alergias = db.Column(db.Text)
    antecedentes = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    id_medico = db.Column(db.String(10), db.ForeignKey('Medico.id_medico'), nullable=False)
    
    # Relaciones
    paciente = db.relationship('Paciente', back_populates='historiales')
    medico = db.relationship('Medico', back_populates='historiales')
    citas = db.relationship('Cita', back_populates='historial')
    
    def __repr__(self):
        return f'<Historial {self.id_historial} - Paciente: {self.dni_paciente}>'