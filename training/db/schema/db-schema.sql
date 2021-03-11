drop database if exists zumbi_train_pipe_db;

create database zumbi_train_pipe_db character set utf8mb4 collate utf8mb4_unicode_ci;

use zumbi_train_pipe_db;

# Store the names of the people who collaborate on the training
create table tb_collaborators(
	id int not null auto_increment,
	cod varchar(50) not null,
	name varchar(50) not null,
	unique(cod),
	primary key(id)
);

create table tb_article_status(
	id int not null auto_increment,
	stat varchar(20) not null,
	dsc varchar(50) not null,
	primary key(id)
);

create table tb_url(
	id int not null auto_increment,
	cod_miner varchar(50),
	url varchar(300) not null,
	art_status int not null default 1,
	unique(url),
	primary key(id),
	foreign key (art_status) references tb_article_status(id)
);

##################
# POPULATE DB
##################

insert into tb_article_status(stat, dsc)
values
	("mined", "URL is collected and recorded into DB"),
	("scraped", "News article is scraped and saved into local DB"),
	("scraped_failed", "News article could not be scraped"),
	("sentencized", "News article is divided into sentences"),
	("sentencized_failed", "News article could not be sentencized");

insert into tb_collaborators(cod, name)
values
	("JOS", "Jeff"),
	("MJ", "Mariana Jansen"),
	("AF", "Anne-Francine"),
	("RA00297726",  "Ana Beatriz Oliveira de Macedo"),
	("RA00297746",	"Bruna Bellini Faria"),
	("RA00275004",	"Douglas Silva de Almeida");