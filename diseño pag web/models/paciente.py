from datetime import date, datetime
from database import db
from sqlalchemy import CheckConstraint
import re

class Paciente(db.Model):
    __tablename__ = 'Paciente'
    
    # Campos principales
    DNI = db.Column(db.String(8), primary_key=True)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    telefono = db.Column(db.String(15))  # Aumentado para incluir código de país (+51)
    direccion = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    tutor_apoderado = db.Column(db.String(100))
    tipo_seguro = db.Column(db.String(20))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    # Constraints de base de datos
    __table_args__ = (
        CheckConstraint("LENGTH(DNI) = 8", name='chk_dni_length'),
        CheckConstraint("DNI NOT GLOB '*[^0-9]*'", name='chk_dni_numeric'),  # Para SQLite
        CheckConstraint("sexo IN ('Masculino', 'Femenino')", name='chk_sexo'),
        CheckConstraint("edad > 0 AND edad <= 120", name='chk_edad'),
        CheckConstraint("tipo_seguro IN ('SIS', 'ESSALUD', 'PRIVADO', 'NINGUNO') OR tipo_seguro IS NULL", name='chk_tipo_seguro'),
        CheckConstraint("correo LIKE '%@%.%' OR correo IS NULL", name='chk_email_format'),
    )

    # Relación con Cita (se definirá cuando creemos el modelo Cita)
    # citas = db.relationship('Cita', backref='paciente', lazy='dynamic')

    def __init__(self, **kwargs):
        # Si se proporciona fecha_nacimiento pero no edad, calcularla automáticamente
        if 'fecha_nacimiento' in kwargs and 'edad' not in kwargs:
            kwargs['edad'] = self.calcular_edad(kwargs['fecha_nacimiento'])
        super().__init__(**kwargs)

    @staticmethod
    def calcular_edad(fecha_nacimiento):
        """Calcula la edad basada en la fecha de nacimiento."""
        if isinstance(fecha_nacimiento, str):
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
        
        today = date.today()
        return today.year - fecha_nacimiento.year - (
            (today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
        )

    @property
    def nombre_completo(self):
        """Retorna el nombre completo del paciente."""
        return f"{self.nombres} {self.apellidos}"

    def validar_dni(self):
        """Valida que el DNI tenga exactamente 8 dígitos numéricos."""
        if not self.DNI:
            raise ValueError("DNI es requerido")
        if len(self.DNI) != 8:
            raise ValueError("DNI debe tener exactamente 8 dígitos")
        if not self.DNI.isdigit():
            raise ValueError("DNI debe contener solo números")
        return True

    def validar_telefono(self):
        """Valida el formato del teléfono."""
        if self.telefono:
            # Remover espacios y caracteres especiales para validación
            telefono_limpio = re.sub(r'[^\d+]', '', self.telefono)
            if not telefono_limpio:
                raise ValueError("Teléfono debe contener al menos números")
            # Validar longitud mínima (9 dígitos para Perú sin código de país)
            numeros_solo = re.sub(r'[^\d]', '', telefono_limpio)
            if len(numeros_solo) < 9:
                raise ValueError("Teléfono debe tener al menos 9 dígitos")
        return True

    def validar_correo(self):
        """Valida el formato del correo electrónico."""
        if self.correo:
            patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(patron_email, self.correo):
                raise ValueError("Formato de correo electrónico inválido")
        return True

    def validar_sexo(self):
        """Valida que el sexo sea uno de los valores permitidos."""
        if self.sexo not in ['Masculino', 'Femenino']:
            raise ValueError("Sexo debe ser 'Masculino' o 'Femenino'")
        return True

    def validar_edad(self):
        """Valida que la edad esté en un rango válido."""
        if not self.edad or self.edad <= 0 or self.edad > 120:
            raise ValueError("Edad debe estar entre 1 y 120 años")
        return True

    def validar_tipo_seguro(self):
        """Valida el tipo de seguro."""
        if self.tipo_seguro and self.tipo_seguro.upper() not in ['SIS', 'ESSALUD', 'PRIVADO', 'NINGUNO']:
            raise ValueError("Tipo de seguro debe ser: SIS, ESSALUD, PRIVADO o NINGUNO")
        return True

    def validar_fecha_nacimiento(self):
        """Valida que la fecha de nacimiento sea coherente con la edad."""
        if self.fecha_nacimiento:
            edad_calculada = self.calcular_edad(self.fecha_nacimiento)
            today = date.today()
            
            # Validar que no sea fecha futura
            if self.fecha_nacimiento > today:
                raise ValueError("La fecha de nacimiento no puede ser futura")
            
            # Validar coherencia con edad si está presente
            if self.edad and abs(edad_calculada - self.edad) > 1:
                raise ValueError("La edad no coincide con la fecha de nacimiento")
        return True

    def validar_completo(self):
        """Ejecuta todas las validaciones del paciente."""
        try:
            self.validar_dni()
            self.validar_telefono()
            self.validar_correo()
            self.validar_sexo()
            self.validar_edad()
            self.validar_tipo_seguro()
            self.validar_fecha_nacimiento()
            return True
        except ValueError as e:
            raise ValueError(f"Error de validación: {str(e)}")

    def actualizar_edad(self):
        """Actualiza la edad basada en la fecha de nacimiento."""
        if self.fecha_nacimiento:
            self.edad = self.calcular_edad(self.fecha_nacimiento)

    def to_dict(self):
        """Convierte el objeto a diccionario para serialización."""
        return {
            'DNI': self.DNI,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'nombre_completo': self.nombre_completo,
            'sexo': self.sexo,
            'edad': self.edad,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'correo': self.correo,
            'tutor_apoderado': self.tutor_apoderado,
            'tipo_seguro': self.tipo_seguro,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }

    @classmethod
    def crear_paciente(cls, **datos):
        """Método de clase para crear un paciente con validaciones."""
        paciente = cls(**datos)
        paciente.validar_completo()
        return paciente

    @classmethod
    def buscar_por_dni(cls, dni):
        """Busca un paciente por DNI."""
        return cls.query.filter_by(DNI=dni).first()

    @classmethod
    def buscar_por_nombre(cls, nombre_busqueda):
        """Busca pacientes por nombre o apellido."""
        return cls.query.filter(
            (cls.nombres.ilike(f'%{nombre_busqueda}%')) |
            (cls.apellidos.ilike(f'%{nombre_busqueda}%'))
        ).all()

    @classmethod
    def listar_por_tipo_seguro(cls, tipo_seguro):
        """Lista pacientes por tipo de seguro."""
        return cls.query.filter_by(tipo_seguro=tipo_seguro.upper()).all()

    def __repr__(self):
        return f'<Paciente {self.DNI} - {self.nombres} {self.apellidos}>'

    def __str__(self):
        return f"{self.nombres} {self.apellidos} (DNI: {self.DNI})"