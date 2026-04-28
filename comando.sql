CREATE DATABASE epis;

USE epis;

CREATE USER 'epi_api_user'@'localhost' IDENTIFIED BY '123Mudar';

GRANT ALL PRIVILEGES ON epis.* TO 'epi_api_user'@'localhost';

CREATE TABLE IF NOT EXISTS epis (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha VARCHAR(32) NOT NULL,
    telefone CHAR(11) NOT NULL UNIQUE,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    status BOOLEAN DEFAULT TRUE,
    tipo ENUM('gestor', 'funcionario') NOT NULL,
    primeiro_acesso BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS sessao (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    expiracao TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL 1 DAY),
    CONSTRAINT fk_usuario_sessao FOREIGN KEY (id_usuario) REFERENCES usuarios (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

INSERT INTO usuarios (nome, email, senha, telefone, usuario, tipo) VALUES ('Luciano Friebe Feigl', 'contatolucianofriebe@gmail.com', '123', '27988610153', 'luciano.feigl', 'gestor');