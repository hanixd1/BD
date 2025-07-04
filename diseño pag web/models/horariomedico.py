from datetime import datetime, time
from database import db
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship

class HorarioMedico(db.Model):
    __tablename__ = 'HorarioMedico'
    
    # Campos principales
    id_horario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_medico = db.Column(db.String(10), db.ForeignKey('Medico.id_medico'), nullable=False)
    dia_semana = db.Column(db.SmallInteger, nullable=False)  # 1=Domingo, 7=Sábado
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    
    # Restricciones de verificación
    __table_args__ = (
        CheckConstraint(
            "dia_semana >= 1 AND dia_semana <= 7",
            name='chk_dia_semana_rango'
        ),
        CheckConstraint(
            "hora_fin > hora_inicio",
            name='chk_horario_valido'
        ),
    )
    
    # Relaciones
    medico = db.relationship('Medico', back_populates='horarios')
    
    # Diccionario para mapear números de día a nombres
    DIAS_SEMANA = {
        1: 'Domingo',
        2: 'Lunes', 
        3: 'Martes',
        4: 'Miércoles',
        5: 'Jueves',
        6: 'Viernes',
        7: 'Sábado'
    }
    
    def __init__(self, id_medico, dia_semana, hora_inicio, hora_fin, activo=True):
        self.id_medico = id_medico
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.activo = activo
    
    @property
    def nombre_dia(self):
        """Devuelve el nombre del día de la semana"""
        return self.DIAS_SEMANA.get(self.dia_semana, 'Desconocido')
    
    @property
    def horario_formateado(self):
        """Devuelve el horario formateado como string"""
        return f"{self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')}"
    
    @property
    def duracion_minutos(self):
        """Calcula la duración del horario en minutos"""
        if isinstance(self.hora_inicio, time) and isinstance(self.hora_fin, time):
            inicio_minutos = self.hora_inicio.hour * 60 + self.hora_inicio.minute
            fin_minutos = self.hora_fin.hour * 60 + self.hora_fin.minute
            return fin_minutos - inicio_minutos
        return 0
    
    def validar_horario(self):
        """Valida que la hora de fin sea posterior a la hora de inicio"""
        if self.hora_fin <= self.hora_inicio:
            return False
        return True
    
    def validar_dia_semana(self):
        """Valida que el día de la semana esté en el rango correcto"""
        return 1 <= self.dia_semana <= 7
    
    def esta_disponible_en_hora(self, hora_consulta):
        """Verifica si el médico está disponible a una hora específica"""
        if not self.activo:
            return False
        
        if isinstance(hora_consulta, str):
            try:
                hora_consulta = datetime.strptime(hora_consulta, '%H:%M').time()
            except ValueError:
                return False
        
        return self.hora_inicio <= hora_consulta <= self.hora_fin
    
    def to_dict(self):
        """Convierte el objeto a diccionario para serialización JSON"""
        return {
            'id_horario': self.id_horario,
            'id_medico': self.id_medico,
            'dia_semana': self.dia_semana,
            'nombre_dia': self.nombre_dia,
            'hora_inicio': self.hora_inicio.strftime('%H:%M') if self.hora_inicio else None,
            'hora_fin': self.hora_fin.strftime('%H:%M') if self.hora_fin else None,
            'horario_formateado': self.horario_formateado,
            'duracion_minutos': self.duracion_minutos,
            'activo': self.activo
        }
    
    @classmethod
    def obtener_por_medico(cls, id_medico, solo_activos=True):
        """Obtiene todos los horarios de un médico específico"""
        query = cls.query.filter_by(id_medico=id_medico)
        if solo_activos:
            query = query.filter_by(activo=True)
        return query.order_by(cls.dia_semana, cls.hora_inicio).all()
    
    @classmethod
    def obtener_por_dia(cls, dia_semana, solo_activos=True):
        """Obtiene todos los horarios de un día específico"""
        query = cls.query.filter_by(dia_semana=dia_semana)
        if solo_activos:
            query = query.filter_by(activo=True)
        return query.order_by(cls.hora_inicio).all()
    
    @classmethod
    def obtener_medicos_disponibles(cls, dia_semana, hora_consulta):
        """Obtiene los médicos disponibles en un día y hora específicos"""
        if isinstance(hora_consulta, str):
            try:
                hora_consulta = datetime.strptime(hora_consulta, '%H:%M').time()
            except ValueError:
                return []
        
        return cls.query.filter(
            cls.dia_semana == dia_semana,
            cls.hora_inicio <= hora_consulta,
            cls.hora_fin >= hora_consulta,
            cls.activo == True
        ).all()
    
    @classmethod
    def verificar_conflicto_horario(cls, id_medico, dia_semana, hora_inicio, hora_fin, id_horario_excluir=None):
        """Verifica si existe conflicto con horarios existentes"""
        query = cls.query.filter(
            cls.id_medico == id_medico,
            cls.dia_semana == dia_semana,
            cls.activo == True
        )
        
        if id_horario_excluir:
            query = query.filter(cls.id_horario != id_horario_excluir)
        
        horarios_existentes = query.all()
        
        for horario in horarios_existentes:
            # Verificar solapamiento
            if (hora_inicio < horario.hora_fin and hora_fin > horario.hora_inicio):
                return True
        
        return False
    
    @classmethod
    def crear_horario_semanal(cls, id_medico, horarios_por_dia):
        """
        Crea horarios para múltiples días de la semana
        horarios_por_dia: dict {dia_semana: [(hora_inicio, hora_fin), ...]}
        """
        horarios_creados = []
        
        for dia, horarios in horarios_por_dia.items():
            for hora_inicio, hora_fin in horarios:
                if not cls.verificar_conflicto_horario(id_medico, dia, hora_inicio, hora_fin):
                    nuevo_horario = cls(
                        id_medico=id_medico,
                        dia_semana=dia,
                        hora_inicio=hora_inicio,
                        hora_fin=hora_fin
                    )
                    horarios_creados.append(nuevo_horario)
        
        return horarios_creados
    
    def __repr__(self):
        return f'<HorarioMedico {self.id_horario} - Médico:{self.id_medico} - {self.nombre_dia} {self.horario_formateado}>'