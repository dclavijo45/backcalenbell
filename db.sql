create schema calenbellback_db;
use calenbellback_db;

create table usuarios(
	id_usuario int primary key auto_increment not null,
	nombres char(20),
	correo varchar(255),
	usuario char(40),
    id_provisional varchar(50) not null,
	password varchar(255) not null
);
create table eventos(
	id int primary key auto_increment not null,
	titulo char(70),
	hora time,
	dia date,
	descripcion varchar(250),
	codigo int not null,
    tipo_ev char(1) not null,
    foreign key (codigo) references usuarios(id_usuario)
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

#alter table eventos add FOREIGN KEY (codigo) REFERENCES usuarios(id_usuario);

#INSERT INTO eventos (titulo, hora, dia, descripcion,codigo) VALUES ('momito', '22:37:22', '2020-09-18', 'cumpleaños del momito',1);