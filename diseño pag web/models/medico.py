from datetime import datetime
from database import db
from sqlalchemy import CheckConstraint
from models.cita import Cita

class Medico(db.Model):
    __tablename__ = 'Medico'
    
    # Campos principales
    id_medico = db.Column(db.String(10), primary_key=True)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    especialidad = db.Column(db.String(50), nullable=False)
    licencia_medica = db.Column(db.String(20), nullable=False, unique=True)
    telefono = db.Column(db.String(15))  # Aumentado para incluir código de país (+51)
    correo_electronico = db.Column(db.String(100))
    horario_disponible = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Restricciones de verificación
    __table_args__ = (
        CheckConstraint(
            "especialidad IN ('Medicina general', 'Pediatría', 'Ginecología', 'Medicina Interna', "
            "'Dermatología', 'Obstetricia', 'Odontología', 'Psicología', 'Traumatología', 'Oftalmología')",
            name='chk_especialidad'
        ),
        CheckConstraint(
            "telefono IS NULL OR LENGTH(telefono) >= 9",
            name='chk_telefono_length'
        ),
        CheckConstraint(
            "correo_electronico IS NULL OR correo_electronico LIKE '%@%.%'",
            name='chk_email_formato'
        ),
    )
    
    # Relaciones
    citas = db.relationship('Cita', back_populates='medico', lazy='dynamic')
    horarios = db.relationship('HorarioMedico', back_populates='medico', lazy='dynamic')
    
    def __init__(self, id_medico, nombres, apellidos, especialidad, licencia_medica, 
                 telefono=None, correo_electronico=None, horario_disponible=None, activo=True):
        self.id_medico = id_medico
        self.nombres = nombres
        self.apellidos = apellidos
        self.especialidad = especialidad
        self.licencia_medica = licencia_medica
        self.telefono = telefono
        self.correo_electronico = correo_electronico
        self.horario_disponible = horario_disponible
        self.activo = activo
    
    @property
    def nombre_completo(self):
        """Devuelve el nombre completo del médico"""
        return f"{self.nombres} {self.apellidos}"
    
    @property
    def citas_activas(self):
        """Devuelve las citas activas (no canceladas) del médico"""
        return self.citas.filter(Cita.estado != 'Cancelada').all()
    
    def validar_email(self):
        """Valida el formato del email"""
        if self.correo_electronico and '@' not in self.correo_electronico:
            return False
        return True
    
    def validar_telefono(self):
        """Valida que el teléfono tenga al menos 9 dígitos"""
        if self.telefono and len(self.telefono) < 9:
            return False
        return True
    
    def to_dict(self):
        """Convierte el objeto a diccionario para serialización JSON"""
        return {
            'id_medico': self.id_medico,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'nombre_completo': self.nombre_completo,
            'especialidad': self.especialidad,
            'licencia_medica': self.licencia_medica,
            'telefono': self.telefono,
            'correo_electronico': self.correo_electronico,
            'horario_disponible': self.horario_disponible,
            'activo': self.activo,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }
    
    @classmethod
    def buscar_por_especialidad(cls, especialidad):
        """Busca médicos activos por especialidad"""
        return cls.query.filter_by(especialidad=especialidad, activo=True).all()
    
    @classmethod
    def buscar_activos(cls):
        """Devuelve todos los médicos activos"""
        return cls.query.filter_by(activo=True).all()
    
    @classmethod
    def buscar_por_id(cls, id_medico):
        """Busca un médico por su ID"""
        return cls.query.filter_by(id_medico=id_medico).first()
    
    def __repr__(self):
        return f'<Medico {self.id_medico} - {self.nombres} {self.apellidos} - {self.especialidad}>'