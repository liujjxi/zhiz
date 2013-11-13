create table if not exists author(
    id int primary key auto_increment,
    name varchar(20),
    email varchar(30),
    description varchar(100),
    url varchar(100)
) engine=innodb default charset=utf8;


create table if not exists blog(
    id int primary key auto_increment,
    name varchar(40),
    description varchar(100),
    disqus varchar(40)
) engine=innodb default charset=utf8;


create table if not exists post(
    id int primary key auto_increment,
    title varchar(40),
    title_pic varchar(100),
    datetime datetime,
    body text
) engine=innodb default charset=utf8;


create table if not exists admin(
    id int primary key auto_increment,
    passwd varchar(33)
) engine=innodb default charset=utf8;


insert into admin set passwd='21232f297a57a5a743894a0e4a801fc3'; /* default passwd: admin */
