from datetime import datetime
from database import db

class CondicionMedica(db.Model):
    __tablename__ = 'CondicionMedica'
    
    id_condicion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_condicion = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(500))
    categoria = db.Column(db.String(50))
    activo = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relación con la tabla Cita (una condición médica puede estar en muchas citas)
    citas = db.relationship('Cita', back_populates='condicion_medica')
    
    def __repr__(self):
        return f'<CondicionMedica {self.id_condicion} - {self.nombre_condicion}>'
    
    def to_dict(self):
        """Convierte el objeto a diccionario para facilitar la serialización"""
        return {
            'id_condicion': self.id_condicion,
            'nombre_condicion': self.nombre_condicion,
            'descripcion': self.descripcion,
            'categoria': self.categoria,
            'activo': self.activo
        }
    
    @staticmethod
    def obtener_activas():
        """Método estático para obtener todas las condiciones médicas activas"""
        return CondicionMedica.query.filter_by(activo=True).all()
    
    @staticmethod
    def obtener_por_categoria(categoria):
        """Método estático para obtener condiciones médicas por categoría"""
        return CondicionMedica.query.filter_by(categoria=categoria, activo=True).all()
    
    @staticmethod
    def crear_condicion(nombre_condicion, descripcion=None, categoria=None):
        """Método estático para crear una nueva condición médica"""
        nueva_condicion = CondicionMedica(
            nombre_condicion=nombre_condicion,
            descripcion=descripcion,
            categoria=categoria
        )
        db.session.add(nueva_condicion)
        return nueva_condicion
    
    def desactivar(self):
        """Método para desactivar una condición médica en lugar de eliminarla"""
        self.activo = False
        db.session.commit()
    
    def activar(self):
        """Método para activar una condición médica"""
        self.activo = True
        db.session.commit()
    
    @staticmethod
    def buscar_por_nombre(nombre):
        """Método estático para buscar condiciones médicas por nombre (búsqueda parcial)"""
        return CondicionMedica.query.filter(
            CondicionMedica.nombre_condicion.ilike(f'%{nombre}%'),
            CondicionMedica.activo == True
        ).all()
    
    @staticmethod
    def obtener_categorias():
        """Método estático para obtener todas las categorías únicas de condiciones médicas activas"""
        categorias = db.session.query(CondicionMedica.categoria).filter_by(activo=True).distinct().all()
        return [categoria[0] for categoria in categorias if categoria[0] is not None]