create schema calenbellback_db;
use calenbellback_db;

create table usuarios(
	id_usuario int primary key auto_increment not null,
	nombres char(20),
	correo varchar(255) unique not null,
	usuario char(40) not null unique,
    id_provisional char(50) unique not null,
    numero char(10) unique null,
    otp_token varchar(100) unique null,
	password varchar(255) not null
);
create table eventos(
	id int primary key auto_increment not null,
	titulo char(70),
	hora time,
	fecha date,
	descripcion varchar(250),
	codigo char(50) not null,
    tipo_ev char(1) not null,
    icono varchar(4),
    foreign key (codigo) references usuarios(id_provisional)
);
create table eventos_grupales(
	id int primary key auto_increment not null,
    idusuario int,
    idevento int,
    foreign key (idusuario) references usuarios(id_usuario),
    foreign key (idevento) references eventos(id)
);
create table usuarios_contactos(
	id_con int primary key auto_increment not null,
    idusuario int,
    id_contacto int,
    foreign key (idusuario) references usuarios(id_usuario),
    foreign key (id_contacto) references usuarios(id_usuario)
);
