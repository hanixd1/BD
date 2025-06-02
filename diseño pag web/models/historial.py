from datetime import datetime
from database import db

class Historial(db.Model):
    __tablename__ = 'Historial'
    
    id_historial = db.Column(db.Integer, primary_key=True, name='ID_HISTORIAL')
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, name='H_FECHA_DE_ACTUALIZACION')
    tratamiento = db.Column(db.Text, name='H_TRATAMIENTO')
    
    # Relación con Cita
    citas = db.relationship('Cita', back_populates='historial')
    
    def __repr__(self):
        return f'<Historial {self.id_historial} - {self.fecha_actualizacion}>'