from datetime import datetime, time
from database import db

class Cita(db.Model):
    __tablename__ = 'Cita'
    
    # Campos principales
    id_cita = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_cita = db.Column(db.String(10), nullable=False, unique=True)  # Formato: 0000012
    dni_paciente = db.Column(db.String(8), db.ForeignKey('Paciente.DNI'), nullable=False)
    id_medico = db.Column(db.String(10), db.ForeignKey('Medico.id_medico'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    motivo = db.Column(db.String(500), nullable=False)
    modalidad = db.Column(db.String(15), nullable=False)  # 'Presencial', 'Remota', 'Visita'
    estado = db.Column(db.String(15), nullable=False, default='Programada')  # 'Programada', 'Completada', 'Cancelada', 'En progreso'
    
    # Campos para la descripción médica
    id_condicion_medica = db.Column(db.Integer, db.ForeignKey('CondicionMedica.id_condicion'))
    descripcion_condicion = db.Column(db.String(500))
    gravedad = db.Column(db.String(15))  # 'Leve', 'Promedio', 'Grave'
    nivel_molestia = db.Column(db.String(15))  # 'Bajo', 'Moderado', 'Molesto'
    persistencia = db.Column(db.String(15))  # 'Corta', 'Media', 'Larga'
    
    # Campos de seguimiento
    fecha_ultima_visita = db.Column(db.Date)
    tiene_visita_previa = db.Column(db.Boolean, default=False)
    observaciones = db.Column(db.String(1000))
    
    # Campos de control
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario_creacion = db.Column(db.String(50))
    
    # Relaciones ORM
    paciente = db.relationship('Paciente', back_populates='citas')
    medico = db.relationship('Medico', back_populates='citas')
    condicion_medica = db.relationship('CondicionMedica', back_populates='citas')
    historial = db.relationship('HistorialCita', back_populates='cita', cascade='all, delete-orphan')
    
    # Restricciones a nivel de modelo (opcional, las principales están en la BD)
    __table_args__ = (
        db.UniqueConstraint('id_medico', 'fecha', 'hora', name='uq_cita_medico_fecha_hora'),
        db.CheckConstraint("modalidad IN ('Presencial', 'Remota', 'Visita')", name='chk_modalidad'),
        db.CheckConstraint("estado IN ('Programada', 'Completada', 'Cancelada', 'En progreso')", name='chk_estado'),
        db.CheckConstraint("gravedad IS NULL OR gravedad IN ('Leve', 'Promedio', 'Grave')", name='chk_gravedad'),
        db.CheckConstraint("nivel_molestia IS NULL OR nivel_molestia IN ('Bajo', 'Moderado', 'Molesto')", name='chk_nivel_molestia'),
        db.CheckConstraint("persistencia IS NULL OR persistencia IN ('Corta', 'Media', 'Larga')", name='chk_persistencia'),
    )
    
    def __init__(self, **kwargs):
        # Generar número de cita automáticamente si no se proporciona
        if 'numero_cita' not in kwargs:
            kwargs['numero_cita'] = self.generar_numero_cita()
        super().__init__(**kwargs)
    
    @staticmethod
    def generar_numero_cita():
        """
        Genera el próximo número de cita automáticamente
        """
        from sqlalchemy import func
        ultimo_numero = db.session.query(func.max(Cita.numero_cita)).scalar()
        if ultimo_numero:
            # Extraer el número y sumar 1
            numero = int(ultimo_numero) + 1
        else:
            numero = 1
        return f"{numero:07d}"  # Formato con 7 dígitos rellenados con ceros
    
    def to_dict(self):
        """
        Convierte el objeto a diccionario para JSON
        """
        return {
            'id_cita': self.id_cita,
            'numero_cita': self.numero_cita,
            'dni_paciente': self.dni_paciente,
            'id_medico': self.id_medico,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'hora': self.hora.strftime('%H:%M:%S') if self.hora else None,
            'motivo': self.motivo,
            'modalidad': self.modalidad,
            'estado': self.estado,
            'id_condicion_medica': self.id_condicion_medica,
            'descripcion_condicion': self.descripcion_condicion,
            'gravedad': self.gravedad,
            'nivel_molestia': self.nivel_molestia,
            'persistencia': self.persistencia,
            'fecha_ultima_visita': self.fecha_ultima_visita.isoformat() if self.fecha_ultima_visita else None,
            'tiene_visita_previa': self.tiene_visita_previa,
            'observaciones': self.observaciones,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_modificacion': self.fecha_modificacion.isoformat() if self.fecha_modificacion else None,
            'usuario_creacion': self.usuario_creacion
        }
    
    def __repr__(self):
        return f'<Cita {self.numero_cita} - {self.fecha} {self.hora} - {self.estado}>'