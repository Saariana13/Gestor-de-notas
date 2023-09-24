CREATE DATABASE [GESTOR_DE_NOTAS_clases_koreano];
GO

USE [GESTOR_DE_NOTAS_clases_koreano];
GO

CREATE TABLE tabla_registros (
    cedula VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    celular VARCHAR(20),
    email VARCHAR(100),
    modalidad VARCHAR(20),
	
);
CREATE TABLE tabla_notas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    cedula_estudiante VARCHAR(10) REFERENCES tabla_registros(cedula),
    pronunciacion FLOAT,
    escritura FLOAT,
    practica FLOAT,
    teoria FLOAT
);

CREATE TABLE [usuarios] (
    [id] INT PRIMARY KEY IDENTITY(1,1),
    [username] VARCHAR(50) NOT NULL,
    [password] VARCHAR(50) NOT NULL
);

select * from  tabla_registros
select * from  tabla_notas
select * from  usuarios 




