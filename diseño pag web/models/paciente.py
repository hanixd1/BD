from datetime import date
from database import db

class Paciente(db.Model):
    __tablename__ = 'Paciente'
    
    dni = db.Column(db.String(8), primary_key=True)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    telefono = db.Column(db.String(9))
    direccion = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    tutor_apoderado = db.Column(db.String(100))
    tipo_seguro = db.Column(db.String(20))

    # Relación con Cita
    
    citas = db.relationship('Cita', backref='paciente', lazy='dynamic')

    @property
    def edad(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    def __repr__(self):
        return f'<Paciente {self.dni} - {self.nombres} {self.apellidos}>'

    def validar(self):
        assert self.dni.isdigit() and len(self.dni) == 8, "DNI inválido"
        if self.telefono:
            assert self.telefono.isdigit() and len(self.telefono) == 9, "Teléfono inválido"
        if self.correo:
            assert "@" in self.correo and "." in self.correo, "Correo inválido"
        if self.tipo_seguro:
            assert self.tipo_seguro.upper() in ['SIS', 'ESSALUD', 'PRIVADO', 'NINGUNO'], "Tipo de seguro inválido"
