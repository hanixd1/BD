CREATE DATABASE GestorSaludRural;
GO

USE GestorSaludRural;
GO

-- Tabla PACIENTE con nuevos campos según interfaz
CREATE TABLE Paciente (
    DNI VARCHAR(8) PRIMARY KEY CHECK (LEN(DNI) = 8 AND DNI NOT LIKE '%[^0-9]%'),
    nombres VARCHAR(50) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    sexo VARCHAR(10) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(9) CHECK (LEN(telefono) = 9 AND telefono NOT LIKE '%[^0-9]%'),
    direccion VARCHAR(100),
    correo VARCHAR(100) CHECK (correo LIKE '%@%.%'),
    tutor_apoderado VARCHAR(100),
    tipo_seguro VARCHAR(20) CHECK (tipo_seguro IN ('SIS', 'ESSALUD', 'PRIVADO', 'NINGUNO')),
    CONSTRAINT CHK_Email_Paciente CHECK (correo IS NULL OR correo LIKE '%@%.%')
);
GO

-- Tabla MÉDICO con licencia médica y otros ajustes
CREATE TABLE Medico (
    id_medico VARCHAR(10) PRIMARY KEY,
    nombres VARCHAR(50) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    especialidad VARCHAR(50) NOT NULL CHECK (especialidad IN (
        'Medicina general', 'Pediatría', 'Ginecología', 'Medicina Interna', 
        'Dermatología', 'Obstetricia', 'Odontología', 'Psicología', 
        'Traumatología', 'Oftalmología', 'Cardiología'
    )),
    licencia_medica VARCHAR(20) NOT NULL UNIQUE,
    telefono VARCHAR(9) CHECK (LEN(telefono) = 9 AND telefono NOT LIKE '%[^0-9]%'),
    correo_electronico VARCHAR(100) CHECK (correo_electronico LIKE '%@%.%'),
    horario_disponible VARCHAR(100)
);
GO

-- Tabla CITA con fecha y hora separadas y nuevos campos
CREATE TABLE Cita (
    id_cita INT IDENTITY(1,1) PRIMARY KEY,
    dni_paciente VARCHAR(8) NOT NULL,
    id_medico VARCHAR(10) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    motivo VARCHAR(200) NOT NULL,
    prioridad VARCHAR(10) NOT NULL CHECK (prioridad IN ('Baja', 'Media', 'Alta', 'Emergencia')),
    estado VARCHAR(15) NOT NULL DEFAULT 'Programada' CHECK (estado IN ('Programada', 'Completada', 'Cancelada', 'En progreso')),
    modalidad VARCHAR(15) NOT NULL CHECK (modalidad IN ('Presencial', 'Remota', 'Visita')),
    nivel_molestia VARCHAR(15) CHECK (nivel_molestia IN ('Bajo', 'Moderado', 'Molesto', 'Severo')),
    persistencia VARCHAR(15) CHECK (persistencia IN ('Corta', 'Media', 'Larga')),
    notas VARCHAR(500),
    ultima_visita DATE,
    intervencion VARCHAR(20),
    
    -- Claves foráneas
    CONSTRAINT FK_Cita_Paciente FOREIGN KEY (dni_paciente) REFERENCES Paciente(DNI),
    CONSTRAINT FK_Cita_Medico FOREIGN KEY (id_medico) REFERENCES Medico(id_medico),
    
    -- Restricción: Un médico no puede tener 2 citas a la misma hora y fecha
    CONSTRAINT UQ_Cita_Medico_Fecha_Hora UNIQUE (id_medico, fecha, hora)
);
GO

-- Tabla para registrar las citas programadas (historial)
CREATE TABLE CitaProgramada (
    id_programacion INT IDENTITY(1,1) PRIMARY KEY,
    id_cita INT NOT NULL,
    fecha_programacion DATETIME DEFAULT GETDATE(),
    usuario_programador VARCHAR(50),
    acciones VARCHAR(100),
    
    CONSTRAINT FK_CitaProgramada_Cita FOREIGN KEY (id_cita) REFERENCES Cita(id_cita)
);
GO

-- Índices para mejorar el rendimiento
CREATE INDEX IX_Paciente_DNI ON Paciente(DNI);
CREATE INDEX IX_Medico_Especialidad ON Medico(especialidad);
CREATE INDEX IX_Cita_Fecha ON Cita(fecha);
CREATE INDEX IX_Cita_Estado ON Cita(estado);
CREATE INDEX IX_Cita_Medico ON Cita(id_medico);
GO

GO
