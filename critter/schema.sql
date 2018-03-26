drop table if exists tweets;
create table tweets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poster_id INTEGER not null,
    poster_name TEXT not null,
    time INTEGER not null,
    text TEXT not null
);
drop table if exists users;
create table users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firebase_id TEXT not null,
    name TEXT not null
);
drop table if exists follows;
create table follows (
    follower INTEGER not null,
    followed INTEGER not null
);
