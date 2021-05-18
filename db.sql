create schema calenbellback_db;
use calenbellback_db;

create table usuarios(
	id_usuario int primary key auto_increment not null,
	nombres char(30) not null,
	correo varchar(255) unique not null,
	usuario char(40) unique not null,
    numero char(10) unique,
	password char(255) not null,
    foto_perfil varchar(150) -- NEW
);
create table eventos(
	id int primary key auto_increment not null,
	titulo char(70) not null,
	hora time not null,
	fecha date not null,
	descripcion varchar(250) not null,
	codigo int not null,
    tipo_ev char(1) not null,
    icono char(1),
    foreign key (codigo) references usuarios(id_usuario)
);
create table eventos_grupales(
	id int primary key auto_increment not null,
    id_usuario int not null,
    id_evento int not null,
    estado_invitacion tinyint(1) not null,
    foreign key (id_usuario) references usuarios(id_usuario),
    foreign key (id_evento) references eventos(id)
);
create table contactos(
    id_usuario int not null,
    id_contacto int not null,
    primary key(id_usuario, id_contacto),
    estado_invitacion tinyint(1) not null,
    foreign key (id_usuario) references usuarios(id_usuario),
    foreign key (id_contacto) references usuarios(id_usuario)
);
