drop table if exists match_assignments;
drop table if exists matches;
drop table if exists player_teams;
drop table if exists match_tables;
drop table if exists coach_certifications;
drop table if exists coaches;
drop table if exists teams;
drop table if exists sponsors;
drop table if exists players;
drop table if exists title;
drop table if exists arbiter_certifications;
drop table if exists arbiters;
drop table if exists managers;
drop table if exists users;
drop table if exists halls;

create table users (
    username varchar(50) not null,
    password varchar(256) not null,
    primary key (username)
);

ALTER TABLE users
  ADD COLUMN role ENUM('manager','player','coach','arbiter') NOT NULL;


create table managers (
    username varchar(50) not null,
    password varchar(256) not null,
    primary key (username),
    foreign key (username)
        references users(username)
        on delete cascade
) engine=innodb;

create table arbiters (
    username          varchar(50)                          not null,
    password          varchar(256)                         not null,
    name              varchar(100)                         not null,
    surname           varchar(100)                         not null,
    nationality       varchar(100)                         not null,
    experience_level  enum('beginner','intermediate','advanced','expert') not null,
    primary key (username),
    foreign key (username)
        references users(username)
        on delete cascade
) engine=innodb;

create table arbiter_certifications (
    username      varchar(50) not null,
    certification varchar(50) not null,
    primary key (username, certification),
    foreign key (username)
        references arbiters(username)
        on delete cascade
) engine=innodb;

create table title (
    title_id   int          not null,
    title_name varchar(50)  not null,
    primary key (title_id)
) engine=innodb;

create table players (
    username     varchar(50) not null,
    password     varchar(256) not null,
    name         varchar(100) not null,
    surname      varchar(100) not null,
    nationality  varchar(100) not null,
    dateofbirth  date        not null,
    elorating    int         not null,
    fideid       varchar(100) not null,
    titleid      int         not null,
    team_list    varchar(50) not null,
    primary key (username),
    foreign key (username) references users(username) on delete cascade,
    foreign key (titleid) references title(title_id),
    check (elorating > 1000)
) engine=innodb;

create table sponsors (
    sponsor_id   int          not null,
    sponsor_name varchar(100) not null,
    primary key (sponsor_id),
    unique key uq_sponsor_name (sponsor_name)
) engine=innodb;

create table teams (
    team_id    int          not null,
    team_name  varchar(100) not null,
    sponsor_id int          not null,
    primary key (team_id),
    foreign key (sponsor_id)
        references sponsors(sponsor_id)
        on update cascade
        on delete restrict
) engine=innodb;

create table coaches (
    username        varchar(50)  not null,
    password        varchar(256) null,
    name            varchar(100) null,
    surname         varchar(100) null,
    nationality     varchar(100) null,
    team_id         int          not null,
    contract_start  date         not null,
    contract_finish date         not null,
    primary key (username, team_id, contract_start, contract_finish),
    foreign key (username)
        references users(username)
        on delete cascade
        on update cascade,
    foreign key (team_id)
        references teams(team_id)
        on update cascade
) engine=innodb;

create table coach_certifications (
    coach_username varchar(50) not null,
    certification   varchar(50) not null,
    primary key (coach_username, certification),
    foreign key (coach_username)
        references coaches(username)
        on delete cascade
        on update cascade
) engine=innodb;

create table halls (
    hall_id       int          not null,
    hall_name     varchar(100) not null,
    hall_country  varchar(50)  not null,
    hall_capacity int          not null,
    primary key (hall_id)
) engine=innodb;

create table match_tables (
    table_id int not null,
    hall_id  int not null,
    primary key (table_id),
    foreign key (hall_id)
        references halls(hall_id)
        on delete cascade
        on update cascade
) engine=innodb;

create table player_teams (
    username varchar(50) not null,
    team_id  int          not null,
    primary key (username, team_id),
    foreign key (username)
        references players(username)
        on delete cascade
        on update cascade,
    foreign key (team_id)
        references teams(team_id)
        on delete cascade
        on update cascade
) engine=innodb;

create table matches (
    match_id         int          not null,
    date             date         not null,
    time_slot        time         not null,
    hall_id          int          not null,
    table_id         int          not null,
    team1_id         int          not null,
    team2_id         int          not null,
    arbiter_username varchar(50)  not null,
    ratings          int          null,
    primary key (match_id),
    foreign key (hall_id)
        references halls(hall_id)
        on delete cascade
        on update cascade,
    foreign key (table_id)
        references match_tables(table_id)
        on delete cascade
        on update cascade,
    foreign key (team1_id)
        references teams(team_id)
        on delete cascade
        on update cascade,
    foreign key (team2_id)
        references teams(team_id)
        on delete cascade
        on update cascade,
    foreign key (arbiter_username)
        references arbiters(username)
        on delete cascade
        on update cascade
) engine=innodb;

create table match_assignments (
    match_id     int                              not null,
    white_player varchar(50)                      not null,
    black_player varchar(50)                      not null,
    result       enum('black wins','white wins','draw') not null,
    primary key (match_id),
    foreign key (match_id)
        references matches(match_id)
        on delete cascade
        on update cascade,
    foreign key (white_player)
        references players(username)
        on delete cascade
        on update cascade,
    foreign key (black_player)
        references players(username)
        on delete cascade
        on update cascade
) engine=innodb;

