drop table if exists tweets;
drop table if exists users;
create table tweets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poster_id INTEGER not null,
    poster_name TEXT not null,
    text TEXT not null
);
create table users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firebase_id TEXT not null,
    name TEXT not null
);
create table follows (
    follower INTEGER not null,
    followed INTEGER not null
);
