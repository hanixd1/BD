CREATE DATABASE PROYECTOGestorSaludRural;
GO

USE PROYECTOGestorSaludRural;
GO


CREATE TABLE [Cita]
( 
	[ID_CITA]            integer  NOT NULL ,
	[CT_FECHA_CITA]      datetime  NULL ,
	[CT_HORA_CITA]       datetime  NULL ,
	[CT_MOTIVO]          varchar(70)  NULL ,
	[CT_PRIORIDAD]       varchar(30)  NULL ,
	[CT_ESTADO]          varchar(30)  NULL ,
	[CT_MODALIDAD]       varchar(30)  NULL ,
	[CT_NIVEL_MOLESTIA]  varchar(30)  NULL ,
	[CT_PERSISTENCIA]    varchar(30)  NULL ,
	[CT_NOTAS]           varchar(70)  NULL ,
	[CT_UTIMA_VISITA]    datetime  NULL ,
	[CT_INTERVENCION]    varchar(50)  NULL ,
	[DNI]                integer  NOT NULL ,
	[ID_HISTORIAL]       integer  NOT NULL ,
	[ID_MEDICO]          integer  NOT NULL 
)
go

CREATE TABLE [Historial]
( 
	[ID_HISTORIAL]       integer  NOT NULL ,
	[H_FECHA_DE_ACTUALIZACION] datetime  NULL ,
	[H_TRATAMIENTO]      varchar(40)  NULL 
)
go

CREATE TABLE [Medico]
( 
	[ID_MEDICO]          integer  NOT NULL ,
	[ME_NOMBRE]          varchar(50)  NULL ,
	[ME_APELLIDO]        varchar(50)  NULL ,
	[ME_ESPECIALIDAD]    varchar(60)  NULL ,
	[ME_LICENCIA]        varchar(40)  NULL ,
	[ME_TELEFONO]        varchar(9)  NULL ,
	[ME_CORREO]          varchar(30)  NULL ,
	[ME_HORARIO]         datetime  NULL 
)
go

CREATE TABLE [Paciente]
( 
	[DNI]                integer  NOT NULL ,
	[PC_NOMBRE]          varchar(50)  NULL ,
	[PC_APELLIDO]        varchar(60)  NULL ,
	[PC_FECHA_NACIMIENTO] datetime  NULL ,
	[PC_DIRECCION]       varchar(50)  NULL ,
	[PC_CORREO]          varchar(70)  NULL ,
	[TIPO_SEGURO]        varchar(30)  NULL ,
	[TUTOR_APODERADO]    varchar(50)  NULL 
)
go

ALTER TABLE [Cita]
	ADD CONSTRAINT [XPKCita] PRIMARY KEY  CLUSTERED ([ID_CITA] ASC)
go

ALTER TABLE [Historial]
	ADD CONSTRAINT [XPKHistorial] PRIMARY KEY  CLUSTERED ([ID_HISTORIAL] ASC)
go

ALTER TABLE [Medico]
	ADD CONSTRAINT [XPKMedico] PRIMARY KEY  CLUSTERED ([ID_MEDICO] ASC)
go

ALTER TABLE [Paciente]
	ADD CONSTRAINT [XPKPaciente] PRIMARY KEY  CLUSTERED ([DNI] ASC)
go


ALTER TABLE [Cita]
	ADD CONSTRAINT [R_1] FOREIGN KEY ([DNI]) REFERENCES [Paciente]([DNI])
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go

ALTER TABLE [Cita]
	ADD CONSTRAINT [R_2] FOREIGN KEY ([ID_HISTORIAL]) REFERENCES [Historial]([ID_HISTORIAL])
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go

ALTER TABLE [Cita]
	ADD CONSTRAINT [R_3] FOREIGN KEY ([ID_MEDICO]) REFERENCES [Medico]([ID_MEDICO])
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go
