from datetime import date
from database import db

class Medico(db.Model):
    __tablename__ = 'Medico'
    
    id_medico = db.Column(db.String(10), primary_key=True)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    especialidad = db.Column(db.String(50), nullable=False)
    licencia_medica = db.Column(db.String(20), nullable=False, unique=True)
    telefono = db.Column(db.String(9))
    correo_electronico = db.Column(db.String(100))
    horario_disponible = db.Column(db.String(100))
    
    # Relación con Cita
    citas = db.relationship('Cita', back_populates='medico')  # ← corregido aquí
    
    def __repr__(self):
        return f'<Medico {self.id_medico} - {self.nombres} {self.apellidos} - {self.especialidad}>'