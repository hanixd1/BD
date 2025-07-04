from datetime import datetime
from database import db

class HistorialCita(db.Model):
    __tablename__ = 'HistorialCita'
    
    id_historial = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cita = db.Column(db.Integer, db.ForeignKey('Cita.id_cita'), nullable=False)
    fecha_accion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    accion = db.Column(db.String(50), nullable=False)  # 'CREADA', 'MODIFICADA', 'CANCELADA', 'COMPLETADA'
    descripcion = db.Column(db.String(200))
    usuario = db.Column(db.String(50))
    
    # Relación con la tabla Cita
    cita = db.relationship('Cita', back_populates='historial_citas')
    
    def __repr__(self):
        return f'<HistorialCita {self.id_historial} - Cita: {self.id_cita} - Acción: {self.accion}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario para facilitar la serialización"""
        return {
            'id_historial': self.id_historial,
            'id_cita': self.id_cita,
            'fecha_accion': self.fecha_accion.isoformat() if self.fecha_accion else None,
            'accion': self.accion,
            'descripcion': self.descripcion,
            'usuario': self.usuario
        }
    
    @staticmethod
    def crear_registro(id_cita, accion, descripcion=None, usuario=None):
        """Método estático para crear un nuevo registro en el historial"""
        nuevo_historial = HistorialCita(
            id_cita=id_cita,
            accion=accion,
            descripcion=descripcion,
            usuario=usuario
        )
        db.session.add(nuevo_historial)
        return nuevo_historial