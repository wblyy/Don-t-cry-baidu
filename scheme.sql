SET SESSION storage_engine = "InnoDB"; 
ALTER DATABASE CHARACTER SET "utf8";

DROP TABLE IF EXISTS ties;
DROP TABLE IF EXISTS sentens;
DROP TABLE IF EXISTS bdusers;

CREATE TABLE bdusers (
    id INT NOT NULL AUTO_INCREMENT,
    username varchar(100) NOT NULL,
    passwd varchar(100) NOT NULL,
    email varchar(100) NOT NULL,

    PRIMARY KEY (id),
    UNIQUE KEY `u_user` (`username`)
);

CREATE TABLE ties (
    id INT NOT NULL AUTO_INCREMENT,
    tieid varchar(255) NOT NULL,
    tietitle varchar(255) NOT NULL,
    baname varchar(255) NOT NULL,
    marks varchar(255) NOT NULL,
    dingcount INT NOT NULL DEFAULT 0,
    totalcount INT NOT NULL DEFAULT 0,
    tiestatus varchar(255) NOT NULL default "normal",
    insertime datetime NOT NULL,
    lastdingtime datetime NOT NULL,
    checktime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY `u_tieid` (`tieid`)
);
CREATE TABLE sentens (
    id INT NOT NULL AUTO_INCREMENT,
    tieid varchar(255) NOT NULL,
    senten varchar(255) NOT NULL,

    PRIMARY KEY (id),
    UNIQUE KEY `u_sen` (`tieid`, `senten`)
);
CREATE TABLE zhidao (
    id INT NOT NULL AUTO_INCREMENT,
    qid varchar(255) NOT NULL,
    senten varchar(255) NOT NULL,
    inserted timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (id)
);